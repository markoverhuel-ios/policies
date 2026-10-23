HAMTrainer screenshots: PLACEHOLDERS ONLY (shot-01 to shot-05, "Screenshot coming").
No real captures exist yet. Do not publish these as final.

To replace: capture 4 to 6 simulator PNGs, put them in
  tools\raw\ham-trainer\   (named 01_home.png, 02_..., in order)
write tools\captions\ham-trainer.json, then run (see tools\README-screenshots.md):
  python tools\frame_screenshots.py --slug ham-trainer --in tools\raw\ham-trainer
The real run deletes the old shot-*.png and shot-*.webp and writes new ones.

Screens to capture (from the app code, UNVERIFIED on device):
1. Home: "Your Progress", questions answered, weakest topic, pool info (HomeView)
2. New Session: Quick Session, Full Pool or One Per Topic, feedback setting (ModeSetupView)
3. Choose Topics: subelements and groups with question counts (ScopePickerView)
4. A quiz question with answers, mid-session (QuizView)
5. Results: your answer versus the correct answer, with "Why" (ResultsView)
6. Optional: Stats, or Browse Pool (StatsView, BrowseView)
Use a pool with no price or purchase text visible (skip the paywall).
