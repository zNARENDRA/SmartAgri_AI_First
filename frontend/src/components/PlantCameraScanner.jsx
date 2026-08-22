import React, { useState, useRef, useEffect } from "react";
import { useFarmer } from "../context/FarmerContext";
import { diagnoseLeafFile } from "../services/api";
import {
  Camera,
  X,
  RotateCcw,
  CheckCircle2,
  AlertTriangle,
  Upload,
  Sparkles,
  RefreshCw,
  Sun,
  Maximize2,
  Image as ImageIcon,
  ShieldCheck,
  SwitchCamera
} from "lucide-react";

export default function PlantCameraScanner({ onScanComplete }) {
  const { showCameraScanner, setShowCameraScanner, setActiveTab } = useFarmer();

  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const cameraInputRef = useRef(null);
  const galleryInputRef = useRef(null);

  const [stream, setStream] = useState(null);
  const [facingMode, setFacingMode] = useState("environment"); // "environment" = rear camera, "user" = front
  const [cameraActive, setCameraActive] = useState(false);
  const [permissionError, setPermissionError] = useState(null);
  const [capturedBlob, setCapturedBlob] = useState(null);
  const [capturedPreview, setCapturedPreview] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [validationWarning, setValidationWarning] = useState(null);

  // Start Camera when modal opens
  useEffect(() => {
    if (showCameraScanner) {
      startCamera(facingMode);
    } else {
      stopCamera();
      resetState();
    }
    return () => {
      stopCamera();
    };
  }, [showCameraScanner, facingMode]);

  const startCamera = async (mode) => {
    stopCamera();
    setPermissionError(null);
    setValidationWarning(null);

    // Check if mediaDevices supported
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      setPermissionError("Camera access is not supported on this browser. Please use gallery upload.");
      return;
    }

    try {
      const constraints = {
        video: {
          facingMode: { ideal: mode },
          width: { ideal: 1280 },
          height: { ideal: 720 }
        },
        audio: false
      };
      const mediaStream = await navigator.mediaDevices.getUserMedia(constraints);
      setStream(mediaStream);
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
        videoRef.current.play();
      }
      setCameraActive(true);
    } catch (err) {
      console.warn("Camera permission or initialization error:", err);
      if (err.name === "NotAllowedError" || err.name === "PermissionDeniedError") {
        setPermissionError("Camera permission was denied. Please allow camera access in your browser settings or upload a photo from your gallery.");
      } else if (err.name === "NotFoundError" || err.name === "DevicesNotFoundError") {
        setPermissionError("No camera device found on your device. Please upload an image from your files.");
      } else {
        setPermissionError("Unable to access camera. Please check permissions or use the gallery fallback below.");
      }
      setCameraActive(false);
    }
  };

  const stopCamera = () => {
    if (stream) {
      stream.getTracks().forEach((track) => track.stop());
      setStream(null);
    }
    setCameraActive(false);
  };

  const resetState = () => {
    setCapturedBlob(null);
    setCapturedPreview(null);
    setAnalyzing(false);
    setPermissionError(null);
    setValidationWarning(null);
  };

  const handleClose = () => {
    stopCamera();
    setShowCameraScanner(false);
    resetState();
  };

  const toggleCameraFacing = () => {
    const nextMode = facingMode === "environment" ? "user" : "environment";
    setFacingMode(nextMode);
  };

  // Capture current video frame to Canvas
  const capturePhoto = () => {
    if (!videoRef.current || !cameraActive) return;

    const video = videoRef.current;
    const canvas = document.createElement("canvas");
    
    // Scale image to a clean max 1024x1024 for fast upload & high clarity
    let w = video.videoWidth || 640;
    let h = video.videoHeight || 480;
    const maxDim = 1024;
    
    if (w > maxDim || h > maxDim) {
      if (w > h) {
        h = Math.round((h * maxDim) / w);
        w = maxDim;
      } else {
        w = Math.round((w * maxDim) / h);
        h = maxDim;
      }
    }

    canvas.width = w;
    canvas.height = h;
    const ctx = canvas.getContext("2d");
    ctx.drawImage(video, 0, 0, w, h);

    // Client-side Quality Validation
    if (w < 120 || h < 120) {
      setValidationWarning("The captured image may be unclear or too small. Try holding the leaf closer with good lighting.");
    } else {
      setValidationWarning(null);
    }

    canvas.toBlob((blob) => {
      if (blob) {
        setCapturedBlob(blob);
        setCapturedPreview(URL.createObjectURL(blob));
        stopCamera();
      }
    }, "image/jpeg", 0.90);
  };

  // Handle Retake
  const handleRetake = () => {
    setCapturedBlob(null);
    setCapturedPreview(null);
    setValidationWarning(null);
    startCamera(facingMode);
  };

  // Handle Gallery/File input fallback
  const handleGalleryUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    // Check size limit (max 12MB)
    if (file.size > 12 * 1024 * 1024) {
      setValidationWarning("File size exceeds 12MB limit. Please select a smaller photo.");
      return;
    }

    setCapturedBlob(file);
    setCapturedPreview(URL.createObjectURL(file));
    setValidationWarning(null);
    stopCamera();
  };

  // Submit image to backend disease detection API
  const handleConfirmAndDiagnose = async () => {
    if (!capturedBlob) return;

    setAnalyzing(true);
    try {
      // Create File from Blob if needed
      const file = capturedBlob instanceof File 
        ? capturedBlob 
        : new File([capturedBlob], "scanned_leaf.jpg", { type: "image/jpeg" });

      const result = await diagnoseLeafFile(file);
      
      // Notify parent or navigate to Disease Detection view with the result
      if (onScanComplete) {
        onScanComplete(result, capturedPreview, file);
      }
      
      setShowCameraScanner(false);
      stopCamera();
      setActiveTab("disease-detection");
    } catch (err) {
      console.error("Diagnosis error:", err);
      setValidationWarning("Diagnosis request failed. Please check network connection and try again.");
    } finally {
      setAnalyzing(false);
    }
  };

  if (!showCameraScanner) return null;

  return (
    <div className="camera-modal-overlay" onClick={handleClose}>
      <div className="camera-modal-content" onClick={(e) => e.stopPropagation()}>
        {/* Header */}
        <div className="camera-modal-header">
          <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
            <div style={{ width: "32px", height: "32px", borderRadius: "8px", background: "#059669", color: "#fff", display: "flex", alignItems: "center", justifyContent: "center" }}>
              <Camera size={18} />
            </div>
            <div>
              <h2 style={{ fontSize: "16px", fontWeight: 800, margin: 0, color: "#ffffff" }}>
                Plant Disease Scanner
              </h2>
              <div style={{ fontSize: "11px", color: "#94a3b8" }}>
                Hold camera steady over affected leaf
              </div>
            </div>
          </div>

          <button
            onClick={handleClose}
            style={{
              background: "rgba(255,255,255,0.15)",
              border: "none",
              color: "#ffffff",
              borderRadius: "50%",
              width: "36px",
              height: "36px",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              cursor: "pointer"
            }}
            aria-label="Close Scanner"
          >
            <X size={20} />
          </button>
        </div>

        {/* Viewfinder / Capture Area */}
        <div className="camera-viewfinder-container">
          {/* Active Live Video Stream */}
          {!capturedPreview && cameraActive && (
            <>
              <video
                ref={videoRef}
                playsInline
                muted
                autoPlay
                className="camera-video-element"
              />

              {/* Viewfinder Target Framing Overlay */}
              <div className="viewfinder-overlay">
                <div className="viewfinder-frame">
                  <div className="viewfinder-corner top-left" />
                  <div className="viewfinder-corner top-right" />
                  <div className="viewfinder-corner bottom-left" />
                  <div className="viewfinder-corner bottom-right" />
                  <div className="viewfinder-scanline" />
                </div>
                <div className="viewfinder-guide-pill">
                  <Sparkles size={13} color="#4ade80" />
                  <span>Place the affected leaf inside the frame</span>
                </div>
              </div>
            </>
          )}

          {/* Captured Preview for Confirmation */}
          {capturedPreview && (
            <div className="camera-preview-container">
              <img
                src={capturedPreview}
                alt="Captured Leaf"
                className="camera-preview-image"
              />
              <div className="preview-confirmation-badge">
                <CheckCircle2 size={15} color="#10b981" />
                <span>Photo Captured • Ready to Diagnose</span>
              </div>
            </div>
          )}

          {/* Permission Error / Native Camera Fallback State */}
          {!capturedPreview && permissionError && (
            <div className="camera-fallback-card" style={{ padding: "40px 20px", textAlign: "center" }}>
              <div style={{ width: "64px", height: "64px", borderRadius: "50%", background: "rgba(16, 185, 129, 0.15)", color: "#10b981", display: "flex", alignItems: "center", justifyContent: "center", margin: "0 auto 16px" }}>
                <Camera size={32} />
              </div>
              <h3 style={{ fontSize: "18px", fontWeight: 800, color: "#ffffff", marginBottom: "8px" }}>
                Launch Device Camera
              </h3>
              <p style={{ fontSize: "13px", color: "#cbd5e1", lineHeight: 1.5, margin: "0 auto 24px auto", maxWidth: "280px" }}>
                {permissionError}
              </p>
              <button
                onClick={() => cameraInputRef.current?.click()}
                className="btn btn-primary"
                style={{ width: "100%", maxWidth: "260px", margin: "0 auto", padding: "14px", fontSize: "15px", background: "linear-gradient(135deg, #10b981 0%, #059669 100%)", display: "flex", justifyContent: "center", gap: "8px" }}
              >
                <Camera size={18} /> <strong>Open Camera / Gallery</strong>
              </button>
            </div>
          )}
        </div>

        {/* Validation Warning Alert */}
        {validationWarning && (
          <div className="camera-warning-banner">
            <AlertTriangle size={16} color="#f59e0b" style={{ flexShrink: 0 }} />
            <span>{validationWarning}</span>
          </div>
        )}

        {/* Action Controls Footer */}
        <div className="camera-modal-footer">
          {/* Hidden File Input for System Camera fallback */}
          <input
            type="file"
            ref={cameraInputRef}
            accept="image/*"
            capture="environment"
            onChange={handleGalleryUpload}
            style={{ display: "none" }}
          />
          {/* Hidden File Input for Gallery fallback */}
          <input
            type="file"
            ref={galleryInputRef}
            accept="image/*"
            onChange={handleGalleryUpload}
            style={{ display: "none" }}
          />

          {!capturedPreview ? (
            /* Live Camera Controls */
            <div className="camera-live-controls">
              {/* Gallery Fallback Button */}
              <button
                onClick={() => galleryInputRef.current?.click()}
                className="camera-btn-secondary"
                title="Upload from Gallery"
              >
                <ImageIcon size={22} />
                <span style={{ fontSize: "11px" }}>Gallery</span>
              </button>

              {/* Big Shutter Capture Button */}
              <button
                onClick={capturePhoto}
                disabled={!cameraActive}
                className="camera-shutter-button"
                aria-label="Capture Leaf Photo"
              >
                <div className="shutter-inner-ring" />
              </button>

              {/* Switch / Flip Camera Button */}
              <button
                onClick={toggleCameraFacing}
                disabled={!cameraActive}
                className="camera-btn-secondary"
                title="Flip Camera"
              >
                <SwitchCamera size={22} />
                <span style={{ fontSize: "11px" }}>Flip</span>
              </button>
            </div>
          ) : (
            /* Confirmation Actions */
            <div className="camera-confirm-controls">
              <button
                onClick={handleRetake}
                disabled={analyzing}
                className="btn btn-secondary"
                style={{ flex: 1, padding: "14px", fontSize: "14px", background: "rgba(255,255,255,0.12)", color: "#ffffff", border: "1px solid rgba(255,255,255,0.2)" }}
              >
                <RotateCcw size={16} /> Retake Photo
              </button>

              <button
                onClick={handleConfirmAndDiagnose}
                disabled={analyzing}
                className="btn btn-primary"
                style={{ flex: 1.5, padding: "14px", fontSize: "14px", background: "linear-gradient(135deg, #10b981 0%, #059669 100%)" }}
              >
                {analyzing ? (
                  <>
                    <RefreshCw size={16} className="spin-animation" />
                    <span>Diagnosing Leaf...</span>
                  </>
                ) : (
                  <>
                    <Sparkles size={16} />
                    <span>Use Photo & Diagnose</span>
                  </>
                )}
              </button>
            </div>
          )}

          {/* Quick Farmer Tips */}
          <div className="camera-tips-row">
            <span>💡 <strong>Tips:</strong> Keep leaf 15-20 cm away • Use good sunlight • Hold steady</span>
          </div>
        </div>
      </div>
    </div>
  );
}
