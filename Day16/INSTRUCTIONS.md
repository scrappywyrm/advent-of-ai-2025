# App Build Plan 🏗️
1. **Structure (`index.html`):**
   - Hero Section with huge Timer (Days, Hours, Mins, Secs).
   - "Did You Know?" Section for rotating facts.
   - Footer with Email Form.
2. **Logic (`script.js`):**
   - `init()`: Check `localStorage` for 'email_signed_up'. Hide form if true.
   - `updateTimer()`: Calc time remaining to Dec 1, 2026. Update DOM. Run every 1s.
   - `rotateFacts()`: Array of 5 facts. Change text every 5s with fade effect.
   - `handleForm()`: On submit, save to localStorage, show success message.
3. **Style (`style.css`):**
   - Background: Dark blue gradient with CSS-only snowfall animation.
   - Cards: White with low opacity and blur (Glassmorphism).
   - Responsive: Stack layout for screens < 600px.
