GROL Trainer screenshots: PLACEHOLDERS ONLY (shot-01 to shot-05, "Screenshot coming").
No real captures exist yet. Do not publish these as final.

To replace: capture 4 to 6 simulator PNGs, put them in
  tools\raw\grol-trainer\   (named 01_home.png, 02_..., in order)
write tools\captions\grol-trainer.json, then run (see tools\README-screenshots.md):
  python tools\frame_screenshots.py --slug grol-trainer --in tools\raw\grol-trainer
The real run deletes the old shot-*.png and shot-*.webp and writes new ones.

Screens to capture (from the app code, UNVERIFIED on device):
1. Home: "Choose an element to practice" with the element list (HomeView)
2. Choose Subsections: subelements and key topics with question counts (SubsectionPickerView)
3. Session setup: mode and "Start Practice" (ModeSetupView)
4. A quiz question mid-session, "Question N of M" (QuizView)
5. Results: score, "By Subsection", "Questions to Review" (ResultsView)
6. Optional: Statistics with "Suggested Review", or Browse Pool (StatsView, BrowseView)
Skip the paywall screen (it shows a price).
