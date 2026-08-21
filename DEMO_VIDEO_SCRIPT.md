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

## 📝 The Script (Target: 8-9 Minutes)

### ⏱️ 0:00 - 1:00 | Introduction & Problem Statement
**[Visual: Start on the SmartAgri AI Landing Page. Scroll slightly to show the beautiful UI.]**

**Speaker:**
> "Hello judges! Welcome to **SmartAgri AI**, an end-to-end, production-grade agricultural decision support platform for Indian farmers. For this hackathon, we didn't just want to build a prototype; we built a fully integrated ecosystem that successfully merges all **five real-world Kaggle datasets** into a single, actionable dashboard.
>
> Our tech stack features a **FastAPI Python backend** powering Scikit-Learn and PyTorch models, paired with a blazing-fast **React and Vite frontend**. Data is stored and indexed in a high-performance **SQLite Relational Database**. Let's jump right into the platform."

---

### ⏱️ 1:00 - 2:30 | Module 1: Crop Advisor & Yield Prediction (Datasets 1 & 3)
**[Visual: Click into the "Farmer Dashboard" and navigate to the "Crop Advisor" tab. Move the sliders for N-P-K.]**

**Speaker:**
> "Here on the Dashboard, the farmer first needs to know *what* to plant.
>
> Using **Dataset 1 (Crop Recommendation)**, our Random Forest classifier achieves 98.8% accuracy. We input real-time soil parameters: Nitrogen, Phosphorus, Potassium, and pH, combined with live weather data. As you can see, the AI confidently recommends [Read the top crop on screen, e.g., 'Rice'] based on these precise conditions.
>
> **[Visual: Switch to the 'Yield Predictor' tab. Show the input fields and click 'Predict Yield']**
>
> "Once the crop is chosen, we switch to our Yield Prediction engine, powered by **Dataset 3 (Crop Yield in India)**. Our Gradient Boosting Regressor analyzes historical state data, rainfall, and fertilizer usage to give the farmer an expected yield in both Quintals per Acre and total Tons. This allows the farmer to calculate expected revenue *before* sowing a single seed."

---

### ⏱️ 2:30 - 4:00 | Module 2: AI Disease Detection (Dataset 2)
**[Visual: Navigate to the "Disease Scanner" tab. Either use the webcam to scan a leaf on your phone, or upload a photo of a diseased leaf from the sample gallery.]**

**Speaker:**
> "During the season, crop health is critical. This brings us to **Dataset 2 (PlantVillage Disease Dataset)**. We trained a Multi-Scale PyTorch Vision Classifier on 27 distinct plant conditions.
>
> A farmer can simply use their mobile camera or upload a photo of a leaf.
>
> **[Visual: Show the model processing and returning a result like 'Tomato Early Blight']**
>
> "Instantly, the model diagnoses the pathogen. But we don't just stop at detection—we provide actionable remediation. The system provides both **organic bio-cures** (like Neem oil) and **chemical fungicides**, complete with exact dosage dilutions and safety intervals. We've brought laboratory-grade agronomy directly to the farmer's pocket."

---

### ⏱️ 4:00 - 5:30 | Module 3: Mandi Market Intelligence (Dataset 4)
**[Visual: Navigate to the "Mandi Prices" tab. Show the cascading dropdowns (State -> District) and the Recharts price trend graph.]**

**Speaker:**
> "Fast forward to harvest time. The biggest question is: *Where should I sell?*
>
> We ingested **Dataset 4 (Daily Wholesale Commodity Prices)**—over 57,000 historical records—into our SQLite database for sub-millisecond querying.
>
> **[Visual: Hover over the trend chart to show modal, min, and max prices.]**
>
> "Farmers can view historical price trends and volatility. More importantly, our **Smart Ranker** algorithm scans neighboring mandis in the state. It might tell the farmer that driving 20 extra kilometers to a different APMC mandi could result in a 15% higher price realization, completely optimizing their logistics and profits."

---

### ⏱️ 5:30 - 6:30 | Module 4: Government Schemes (Dataset 5)
**[Visual: Navigate to the "Govt Schemes" tab. Show how the profile matches the schemes.]**

**Speaker:**
> "Beyond the market, farmers often miss out on crucial financial support. Using **Dataset 5 (Indian Government Schemes)**, we built a Semantic Profile Eligibility Matcher.
>
> Based on the farmer's profile—their landholding size, tier, state, and current crop—the system filters out irrelevant noise and ranks the highest-matching subsidies.
>
> **[Visual: Click on a scheme to expand the details.]**
>
> "It tells them exactly what documents are needed and provides a direct, verified link to the official MyScheme.gov.in portal. We prioritized ethical AI here: no false promises, just verified government links."

---

### ⏱️ 6:30 - 8:00 | The Masterpiece: AI Assistant & Farm Action Plan
**[Visual: Click the "Action Plan" button (usually the amber button on the dashboard) and wait for the confetti/modal to appear.]**

**Speaker:**
> "Finally, we tied all these complex machine-learning models together. The average farmer doesn't want to check five different tabs.
>
> By clicking **Generate Action Plan**, our backend synthesizes all live data—soil, weather, mandi prices, and plant health—into a single **8-point Farm Action Plan**. It tells them what to plant, when to irrigate based on the 7-day Open-Meteo forecast, disease risks to watch out for, and where to sell.
>
> **[Visual: Close the plan, open the AI Assistant Chat in the bottom right, and type a question like: "Is it safe to spray fungicide today?"]**
>
> "And if they have specific questions, our Central AI Assistant acts as an orchestrator. It seamlessly connects to the weather API and our models to answer in natural language."

---

### ⏱️ 8:00 - 9:00 | Conclusion & Architecture
**[Visual: Pull up the Architecture diagram from the README.md or just show the clean code structure in VS Code.]**

**Speaker:**
> "To summarize, SmartAgri AI is not a mockup. It is a fully functional, container-ready platform.
>
> *   **Innovation:** We combined 5 disparate datasets into one unified workflow.
> *   **Technical Implementation:** We used FastAPI, React, and PyTorch, ensuring high scalability.
> *   **Feasibility:** It runs efficiently on standard infrastructure and is designed for mobile-first access.
>
> All code is thoroughly documented, and our GitHub repository includes automated setup scripts so judges can launch this locally with one click. Thank you for your time, and we believe SmartAgri AI is the comprehensive solution Indian farmers need today."
