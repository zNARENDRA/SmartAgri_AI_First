# 🎥 Hackathon Demo Video Script: SmartAgri AI

**Overall Tips for Recording:**
*   **Keep it moving:** Don't linger too long on one screen; keep the pace energetic.
*   **Split screen or picture-in-picture:** Have your face in the corner (if comfortable) and record your screen clearly at 1080p.
*   **Pre-load data:** Have the local server running and the datasets already seeded so you don't waste time waiting for things to load.

## 🛠️ Recommended Tools for Recording
*   **OBS Studio (Best & Free):** Download from obsproject.com. It allows you to easily capture your screen and webcam at the same time, giving a professional look.
*   **Loom (Easiest):** A Chrome extension/app that records your screen and camera simultaneously and instantly uploads it to the cloud. You can download the video afterward.
*   **Zoom/Google Meet:** Start a private meeting, share your screen, turn on your camera, and hit record.

---

## 📝 The Script (Target: 5-6 Minutes)

### ⏱️ 0:00 - 0:45 | Intro & Overview
**[Visual: Start on the SmartAgri AI Landing Page. Scroll quickly to show the UI.]**

**Speaker:**
> "Hello judges! Welcome to **SmartAgri AI**, a production-grade agricultural decision platform for Indian farmers. We successfully merged all **five real-world Kaggle datasets** into a single dashboard powered by a Python FastAPI backend and a React frontend. Let's jump into the demo."

---

### ⏱️ 0:45 - 1:45 | Crop & Yield (Datasets 1 & 3)
**[Visual: Go to Farmer Dashboard -> 'Crop Advisor' tab, tweak a slider. Then click 'Yield Predictor'.]**

**Speaker:**
> "Using **Dataset 1 (Crop Recommendation)**, our Random Forest model analyzes live soil N-P-K, pH, and weather to recommend the ideal crop—like Rice—with 98% accuracy. 
> 
> Once the crop is chosen, our Yield Predictor, powered by **Dataset 3 (Crop Yield)**, uses Gradient Boosting to forecast the exact yield in Quintals per Acre based on acreage, rainfall, and fertilizer usage, so farmers can plan their revenue before sowing."

---

### ⏱️ 1:45 - 2:45 | AI Disease Scanner (Dataset 2)
**[Visual: Go to 'Disease Scanner'. Upload a leaf photo or use the camera demo.]**

**Speaker:**
> "For crop health, we integrated **Dataset 2 (PlantVillage)** into a PyTorch Vision Classifier. Farmers simply scan a leaf with their phone. 
> 
> **[Visual: Show diagnosis result]**
>
> The AI instantly detects the pathogen—like Early Blight—and provides both organic bio-cures and chemical fungicides with exact dosage dilutions."

---

### ⏱️ 2:45 - 3:45 | Mandi Market Intelligence (Dataset 4)
**[Visual: Go to 'Mandi Prices'. Show the trend chart and the 'Where to Sell' card.]**

**Speaker:**
> "At harvest, farmers need to know where to sell. We ingested over 57,000 historical price records from **Dataset 4 (Mandi Prices)**. 
>
> Farmers can see live trends, but our standout feature is the **Smart Ranker**. It scans neighboring APMC mandis to tell the farmer if driving 20 extra kilometers will yield a higher profit."

---

### ⏱️ 3:45 - 5:00 | Government Schemes & The Action Plan (Dataset 5)
**[Visual: Briefly click 'Govt Schemes', then hit the big 'Action Plan' button to generate the report.]**

**Speaker:**
> "We also use **Dataset 5 (Govt Schemes)** to match the farmer's landholding profile to eligible subsidies, providing verified links to MyScheme.gov.in. 
> 
> **[Visual: Scroll through the generated Action Plan, then open the AI Assistant Chat in the corner]**
>
> But farmers don't want to check five tabs. By clicking **Generate Action Plan**, our engine synthesizes all live data into a single 8-point checklist. And if they have questions, they can chat with our natural language AI assistant, which orchestrates these tools seamlessly."

---

### ⏱️ 5:00 - 6:00 | Outro & Architecture
**[Visual: Show the GitHub repo or the run.bat file in VS Code.]**

**Speaker:**
> "SmartAgri AI is not just a mockup—it's a high-performance system using SQLite for sub-millisecond queries. We've included a one-click `run.bat` script in our GitHub repo so you can launch the entire stack locally. 
>
> Thank you for your time, and we believe this is the comprehensive AI solution Indian farmers need today."
