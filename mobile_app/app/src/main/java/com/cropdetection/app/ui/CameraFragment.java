package com.cropdetection.app.ui;

import android.Manifest;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;

import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.camera.core.CameraSelector;
import androidx.camera.core.ImageCapture;
import androidx.camera.core.ImageCaptureException;
import androidx.camera.core.ImageProxy;
import androidx.camera.core.Preview;
import androidx.camera.lifecycle.ProcessCameraProvider;
import androidx.camera.view.PreviewView;
import androidx.core.content.ContextCompat;
import androidx.fragment.app.Fragment;
import androidx.navigation.Navigation;

import com.cropdetection.app.R;
import com.cropdetection.app.api.ApiClient;
import com.cropdetection.app.api.DiseaseResult;
import com.google.android.material.button.MaterialButton;
import com.google.common.util.concurrent.ListenableFuture;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.util.concurrent.ExecutionException;

import okhttp3.MediaType;
import okhttp3.MultipartBody;
import okhttp3.RequestBody;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class CameraFragment extends Fragment {
    
    private static final String TAG = "CameraFragment";
    private static final String[] REQUIRED_PERMISSIONS = {Manifest.permission.CAMERA};
    
    private PreviewView viewFinder;
    private MaterialButton captureButton;
    private View loadingOverlay;
    private ProgressBar progressBar;
    private TextView statusText;
    
    private ImageCapture imageCapture;
    private ProcessCameraProvider cameraProvider;
    
    private final ActivityResultLauncher<String> requestPermissionLauncher =
            registerForActivityResult(new ActivityResultContracts.RequestPermission(), isGranted -> {
                if (isGranted) {
                    startCamera();
                } else {
                    Toast.makeText(requireContext(), 
                            R.string.camera_permission_denied, 
                            Toast.LENGTH_SHORT).show();
                }
            });

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container,
                             @Nullable Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_camera, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);
        
        viewFinder = view.findViewById(R.id.viewFinder);
        captureButton = view.findViewById(R.id.captureButton);
        loadingOverlay = view.findViewById(R.id.loadingOverlay);
        progressBar = view.findViewById(R.id.progressBar);
        statusText = view.findViewById(R.id.statusText);
        
        if (allPermissionsGranted()) {
            startCamera();
        } else {
            requestPermissionLauncher.launch(Manifest.permission.CAMERA);
        }
        
        captureButton.setOnClickListener(v -> captureImage());
    }

    private boolean allPermissionsGranted() {
        for (String permission : REQUIRED_PERMISSIONS) {
            if (ContextCompat.checkSelfPermission(requireContext(), permission)
                    != PackageManager.PERMISSION_GRANTED) {
                return false;
            }
        }
        return true;
    }

    private void startCamera() {
        ListenableFuture<ProcessCameraProvider> cameraProviderFuture =
                ProcessCameraProvider.getInstance(requireContext());

        cameraProviderFuture.addListener(() -> {
            try {
                cameraProvider = cameraProviderFuture.get();
                bindCameraUseCases();
            } catch (ExecutionException | InterruptedException e) {
                Log.e(TAG, "Error starting camera", e);
            }
        }, ContextCompat.getMainExecutor(requireContext()));
    }

    private void bindCameraUseCases() {
        Preview preview = new Preview.Builder().build();
        preview.setSurfaceProvider(viewFinder.getSurfaceProvider());

        imageCapture = new ImageCapture.Builder()
                .setCaptureMode(ImageCapture.CAPTURE_MODE_MINIMIZE_LATENCY)
                .build();

        CameraSelector cameraSelector = CameraSelector.DEFAULT_BACK_CAMERA;

        try {
            cameraProvider.unbindAll();
            cameraProvider.bindToLifecycle(
                    getViewLifecycleOwner(),
                    cameraSelector,
                    preview,
                    imageCapture
            );
        } catch (Exception e) {
            Log.e(TAG, "Use case binding failed", e);
        }
    }

    private void captureImage() {
        if (imageCapture == null) return;

        captureButton.setEnabled(false);
        showLoading(true);

        imageCapture.takePicture(
                ContextCompat.getMainExecutor(requireContext()),
                new ImageCapture.OnImageCapturedCallback() {
                    @Override
                    public void onCaptureSuccess(@NonNull ImageProxy image) {
                        Bitmap bitmap = imageProxyToBitmap(image);
                        image.close();
                        
                        if (bitmap != null) {
                            uploadImage(bitmap);
                        } else {
                            showError("Failed to process image");
                            captureButton.setEnabled(true);
                            showLoading(false);
                        }
                    }

                    @Override
                    public void onError(@NonNull ImageCaptureException exception) {
                        Log.e(TAG, "Photo capture failed", exception);
                        showError("Capture failed: " + exception.getMessage());
                        captureButton.setEnabled(true);
                        showLoading(false);
                    }
                }
        );
    }

    private Bitmap imageProxyToBitmap(ImageProxy image) {
        ByteBuffer buffer = image.getPlanes()[0].getBuffer();
        byte[] bytes = new byte[buffer.remaining()];
        buffer.get(bytes);
        return BitmapFactory.decodeByteArray(bytes, 0, bytes.length);
    }

    private void uploadImage(Bitmap bitmap) {
        try {
            File file = bitmapToFile(bitmap);
            RequestBody requestFile = RequestBody.create(MediaType.parse("image/jpeg"), file);
            MultipartBody.Part body = MultipartBody.Part.createFormData("image", file.getName(), requestFile);
            RequestBody language = RequestBody.create(MediaType.parse("text/plain"), "en");

            ApiClient.getApiService().predictDisease(body, language).enqueue(new Callback<DiseaseResult>() {
                @Override
                public void onResponse(@NonNull Call<DiseaseResult> call, @NonNull Response<DiseaseResult> response) {
                    captureButton.setEnabled(true);
                    showLoading(false);
                    
                    if (response.isSuccessful() && response.body() != null) {
                        navigateToResults(response.body(), bitmap);
                    } else {
                        showError("Server error: " + response.code());
                    }
                }

                @Override
                public void onFailure(@NonNull Call<DiseaseResult> call, @NonNull Throwable t) {
                    captureButton.setEnabled(true);
                    showLoading(false);
                    showError("Network error: " + t.getMessage());
                    
                    // Use mock data for testing
                    useMockData(bitmap);
                }
            });
        } catch (IOException e) {
            Log.e(TAG, "Error uploading image", e);
            showError("Upload failed");
            captureButton.setEnabled(true);
            showLoading(false);
        }
    }

    private File bitmapToFile(Bitmap bitmap) throws IOException {
        File file = new File(requireContext().getCacheDir(), "captured_image.jpg");
        ByteArrayOutputStream bos = new ByteArrayOutputStream();
        bitmap.compress(Bitmap.CompressFormat.JPEG, 80, bos);
        byte[] bitmapData = bos.toByteArray();

        FileOutputStream fos = new FileOutputStream(file);
        fos.write(bitmapData);
        fos.flush();
        fos.close();
        return file;
    }

    private void useMockData(Bitmap bitmap) {
        DiseaseResult mockResult = new DiseaseResult(
                "Tomato Early Blight",
                0.95f,
                "Early blight is a common fungal disease affecting tomato plants. It causes dark spots on leaves and can reduce crop yield.",
                "Remove infected leaves, apply copper-based fungicide, ensure proper spacing for air circulation, and avoid overhead watering."
        );
        navigateToResults(mockResult, bitmap);
    }

    private void navigateToResults(DiseaseResult result, Bitmap bitmap) {
        Bundle bundle = ResultsFragment.createBundle(result, bitmap);
        Navigation.findNavController(requireView())
                .navigate(R.id.action_camera_to_results, bundle);
    }

    private void showLoading(boolean show) {
        loadingOverlay.setVisibility(show ? View.VISIBLE : View.GONE);
    }

    private void showError(String message) {
        Toast.makeText(requireContext(), message, Toast.LENGTH_SHORT).show();
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        if (cameraProvider != null) {
            cameraProvider.unbindAll();
        }
    }
}
