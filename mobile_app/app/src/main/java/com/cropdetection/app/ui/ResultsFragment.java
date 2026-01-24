package com.cropdetection.app.ui;

import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.media.AudioAttributes;
import android.media.MediaPlayer;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.navigation.Navigation;

import com.cropdetection.app.R;
import com.cropdetection.app.api.ApiClient;
import com.cropdetection.app.api.AudioResponse;
import com.cropdetection.app.api.DiseaseResult;
import com.google.android.material.button.MaterialButton;

import java.io.ByteArrayOutputStream;
import java.io.IOException;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class ResultsFragment extends Fragment {
    
    private static final String TAG = "ResultsFragment";
    private static final String ARG_RESULT = "disease_result";
    private static final String ARG_IMAGE = "captured_image";
    
    private ImageView capturedImage;
    private TextView diseaseName;
    private TextView confidence;
    private TextView description;
    private TextView treatment;
    private Spinner languageSpinner;
    private MaterialButton playAudioButton;
    private MaterialButton backButton;
    
    private DiseaseResult diseaseResult;
    private Bitmap imageBitmap;
    private MediaPlayer mediaPlayer;
    private String selectedLanguage = "en";
    private boolean isPlaying = false;
    
    private final String[] languages = {
            "English", "हिंदी (Hindi)", "मराठी (Marathi)", "தமிழ் (Tamil)",
            "తెలుగు (Telugu)", "ગુજરાતી (Gujarati)", "ਪੰਜਾਬੀ (Punjabi)", "বাংলা (Bengali)"
    };
    
    private final String[] languageCodes = {
            "en", "hi", "mr", "ta", "te", "gu", "pa", "bn"
    };

    public static Bundle createBundle(DiseaseResult result, Bitmap bitmap) {
        Bundle bundle = new Bundle();
        bundle.putSerializable(ARG_RESULT, result);
        
        ByteArrayOutputStream stream = new ByteArrayOutputStream();
        bitmap.compress(Bitmap.CompressFormat.PNG, 100, stream);
        bundle.putByteArray(ARG_IMAGE, stream.toByteArray());
        
        return bundle;
    }

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container,
                             @Nullable Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_results, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);
        
        initViews(view);
        loadArguments();
        setupLanguageSpinner();
        setupListeners();
        displayResults();
    }

    private void initViews(View view) {
        capturedImage = view.findViewById(R.id.capturedImage);
        diseaseName = view.findViewById(R.id.diseaseName);
        confidence = view.findViewById(R.id.confidence);
        description = view.findViewById(R.id.description);
        treatment = view.findViewById(R.id.treatment);
        languageSpinner = view.findViewById(R.id.languageSpinner);
        playAudioButton = view.findViewById(R.id.playAudioButton);
        backButton = view.findViewById(R.id.backButton);
    }

    private void loadArguments() {
        if (getArguments() != null) {
            diseaseResult = (DiseaseResult) getArguments().getSerializable(ARG_RESULT);
            byte[] imageBytes = getArguments().getByteArray(ARG_IMAGE);
            if (imageBytes != null) {
                imageBitmap = BitmapFactory.decodeByteArray(imageBytes, 0, imageBytes.length);
            }
        }
    }

    private void setupLanguageSpinner() {
        ArrayAdapter<String> adapter = new ArrayAdapter<>(
                requireContext(),
                android.R.layout.simple_spinner_item,
                languages
        );
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        languageSpinner.setAdapter(adapter);
        
        languageSpinner.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
                selectedLanguage = languageCodes[position];
                stopAudio();
            }

            @Override
            public void onNothingSelected(AdapterView<?> parent) {
            }
        });
    }

    private void setupListeners() {
        playAudioButton.setOnClickListener(v -> {
            if (isPlaying) {
                stopAudio();
            } else {
                playAudio();
            }
        });
        
        backButton.setOnClickListener(v -> 
                Navigation.findNavController(v).navigate(R.id.action_results_to_camera));
    }

    private void displayResults() {
        if (diseaseResult != null) {
            diseaseName.setText(diseaseResult.getDiseaseName());
            confidence.setText(diseaseResult.getConfidencePercentage());
            description.setText(diseaseResult.getDescription());
            treatment.setText(diseaseResult.getTreatment());
        }
        
        if (imageBitmap != null) {
            capturedImage.setImageBitmap(imageBitmap);
        }
    }

    private void playAudio() {
        if (diseaseResult == null) return;
        
        String audioText = String.format(
                "Disease: %s. Confidence: %s. Description: %s. Treatment: %s",
                diseaseResult.getDiseaseName(),
                diseaseResult.getConfidencePercentage(),
                diseaseResult.getDescription(),
                diseaseResult.getTreatment()
        );
        
        // Try to get audio from API
        ApiClient.getApiService().generateAudio(audioText, selectedLanguage)
                .enqueue(new Callback<AudioResponse>() {
                    @Override
                    public void onResponse(@NonNull Call<AudioResponse> call, 
                                         @NonNull Response<AudioResponse> response) {
                        if (response.isSuccessful() && response.body() != null) {
                            String audioUrl = response.body().getAudioUrl();
                            playAudioFromUrl(audioUrl);
                        } else {
                            showMockAudioMessage();
                        }
                    }

                    @Override
                    public void onFailure(@NonNull Call<AudioResponse> call, @NonNull Throwable t) {
                        Log.e(TAG, "Audio generation failed", t);
                        showMockAudioMessage();
                    }
                });
    }

    private void playAudioFromUrl(String url) {
        try {
            if (mediaPlayer != null) {
                mediaPlayer.release();
            }
            
            mediaPlayer = new MediaPlayer();
            mediaPlayer.setAudioAttributes(
                    new AudioAttributes.Builder()
                            .setContentType(AudioAttributes.CONTENT_TYPE_SPEECH)
                            .setUsage(AudioAttributes.USAGE_MEDIA)
                            .build()
            );
            
            mediaPlayer.setDataSource(url);
            mediaPlayer.setOnPreparedListener(mp -> {
                mp.start();
                isPlaying = true;
                updatePlayButton();
            });
            
            mediaPlayer.setOnCompletionListener(mp -> {
                isPlaying = false;
                updatePlayButton();
            });
            
            mediaPlayer.setOnErrorListener((mp, what, extra) -> {
                Log.e(TAG, "MediaPlayer error: " + what);
                isPlaying = false;
                updatePlayButton();
                return false;
            });
            
            mediaPlayer.prepareAsync();
            
        } catch (IOException e) {
            Log.e(TAG, "Error playing audio", e);
            Toast.makeText(requireContext(), "Error playing audio", Toast.LENGTH_SHORT).show();
        }
    }

    private void showMockAudioMessage() {
        Toast.makeText(requireContext(), 
                "Audio playback in " + languages[getLanguageIndex()] + " (Mock mode)", 
                Toast.LENGTH_LONG).show();
        
        // Simulate audio playing
        isPlaying = true;
        updatePlayButton();
        
        requireView().postDelayed(() -> {
            isPlaying = false;
            updatePlayButton();
        }, 3000);
    }

    private int getLanguageIndex() {
        for (int i = 0; i < languageCodes.length; i++) {
            if (languageCodes[i].equals(selectedLanguage)) {
                return i;
            }
        }
        return 0;
    }

    private void stopAudio() {
        if (mediaPlayer != null) {
            if (mediaPlayer.isPlaying()) {
                mediaPlayer.stop();
            }
            mediaPlayer.release();
            mediaPlayer = null;
        }
        isPlaying = false;
        updatePlayButton();
    }

    private void updatePlayButton() {
        if (isPlaying) {
            playAudioButton.setText(R.string.stop_audio);
            playAudioButton.setIcon(requireContext().getDrawable(android.R.drawable.ic_media_pause));
        } else {
            playAudioButton.setText(R.string.play_audio);
            playAudioButton.setIcon(requireContext().getDrawable(android.R.drawable.ic_media_play));
        }
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        stopAudio();
    }
}
