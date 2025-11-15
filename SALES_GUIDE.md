# 🎯 Sales Team - Tangram Challenge Deployment Checklist

## 📦 OPTION A: For Trade Shows / Live Demos

**Preparation Time**: 30 minutes (one-time)  
**Demo Time**: 2 minutes  
**Customer Setup**: 0 minutes

### Before the Show

- [ ] Run `build.bat` on your laptop (builds all .exe files)
- [ ] Copy `portable_package` folder to 3+ USB drives
- [ ] Test on a clean Windows PC (not your dev machine)
- [ ] Bring backup USB drives
- [ ] Pack tangram pieces (7 colors)
- [ ] Bring USB webcam (in case booth PC camera doesn't work)
- [ ] Print 5 copies of quick reference card (below)

### At the Booth

1. **Setup (5 minutes)**
   - Plug USB drive into demo PC
   - Position camera looking down at desk
   - Place tangram pieces within view
   - Double-click `TangramLauncher.exe`
   - Click "Test Camera" to verify

2. **Demo Script (2 minutes)**
   ```
   [Show customer the colored tangram pieces]
   "These are standard tangram puzzle pieces. Kids play with them physically."
   
   [Click "Play Game"]
   "The software uses a camera to detect the pieces in real-time."
   
   [Point to screen showing target shape]
   "The game shows what shape to make - like this swan."
   
   [Move pieces around]
   "As the child arranges the physical pieces, the score updates immediately.
   They get instant feedback without staring at a screen!"
   
   [Point to cartoon pieces on screen]
   "The camera view is hidden - kids see these fun cartoon shapes instead.
   This keeps them focused on hands-on learning."
   
   [Click Shape Editor]
   "Parents and teachers can create unlimited custom shapes."
   
   "Perfect for ages 4-12, develops spatial reasoning and problem-solving."
   ```

3. **Giveaway (Optional)**
   - Hand customer a USB drive with the portable package
   - "Try it at home! Just plug in and run - no installation needed."

### Pros
✅ Zero installation at booth  
✅ Works offline  
✅ Can demo on any Windows PC  
✅ Easy to give customers copies  

---

## 📦 OPTION B: For Remote Sales / Customer Delivery

**Preparation Time**: 5 minutes (one-time)  
**Customer Setup**: 2-5 minutes  
**Professional appearance**: ⭐⭐⭐⭐⭐

### Preparation

1. **Build the installer** (one-time):
   ```
   - Run build.bat
   - Install Inno Setup (free)
   - Compile tangram_installer.iss
   - Get: TangramChallenge_Setup.exe
   ```

2. **Upload to cloud**:
   - Upload `TangramChallenge_Setup.exe` to Dropbox/Google Drive/OneDrive
   - Create shareable link
   - Save link for future use

### During Sales Call

1. **Send link in chat**: 
   ```
   "I'm sending you a download link now. 
   It's a 2-minute install while we talk."
   ```

2. **Guide installation**:
   ```
   Customer: "I've downloaded it"
   You: "Great! Double-click to install, then click Next a couple times"
   [Wait 1-2 minutes]
   Customer: "It's installed"
   You: "Perfect! Look for 'Tangram Challenge' in your Start Menu"
   ```

3. **Demo remotely**:
   ```
   "Click 'Test Camera' first to check your webcam"
   "Now click 'Play Game'"
   "Do you see the swan shape on screen?"
   [Walk through demo]
   ```

4. **Follow-up**:
   ```
   "It's now installed on your PC. 
   Feel free to try it with kids and let me know what you think!"
   ```

### Pros
✅ Professional installation experience  
✅ Appears in Start Menu  
✅ Customer has it to try later  
✅ Includes uninstaller  

---

## 📋 Quick Reference Card (Print & Laminate)

```
┌─────────────────────────────────────────────────────┐
│         🎮 TANGRAM CHALLENGE - QUICK START          │
├─────────────────────────────────────────────────────┤
│                                                     │
│  1. Position camera looking DOWN at desk            │
│  2. Double-click TangramLauncher.exe                │
│  3. Click "Test Camera" button                      │
│  4. Place 7 colored tangram pieces on desk          │
│  5. Click "Play Game"                               │
│                                                     │
│  GAME CONTROLS:                                     │
│    SPACE - Pause        R - Reset                   │
│    N - Next shape       ESC - Quit                  │
│                                                     │
│  CAMERA TIPS:                                       │
│    ✓ Bright, even lighting                          │
│    ✓ Light-colored desk                             │
│    ✓ No shadows on pieces                           │
│    ✓ Camera 1-2 feet above desk                     │
│                                                     │
│  TROUBLESHOOTING:                                   │
│    Pieces not detected? → Calibrate Camera          │
│    Game slow? → Close other programs                │
│    Need help? → See README.md                       │
│                                                     │
│  REQUIRED PIECES:                                   │
│    🔴 Red 🔵 Blue 🟢 Green 🟠 Orange                │
│    🟡 Yellow 🟣 Purple 🔵 Teal                       │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 🎯 Common Objections & Responses

### "Do we need to install Python?"
**Response**: "No! It's a standalone .exe file. Double-click and it runs. No Python, no dependencies, nothing to install except the app itself."

### "Is this complicated to set up?"
**Response**: "Not at all! [Show them launching it] See? Double-click, and it opens. The hardest part is positioning the camera, which takes 30 seconds."

### "What if we don't have tangram pieces?"
**Response**: "You can buy a set for $10 on Amazon, or make your own from colored cardboard. We include a guide showing exactly how."

### "Will this work with our existing webcams?"
**Response**: "Yes, any USB webcam works. Even built-in laptop cameras work if you angle the laptop right. Want to test with your camera right now?"

### "Do kids need computer skills?"
**Response**: "Zero! They play with physical pieces on a desk - just like regular tangram puzzles. The computer just watches and gives them feedback. They never even touch the keyboard."

### "Can teachers create their own puzzles?"
**Response**: "[Click Shape Editor] See this? Drag the pieces around, make any shape you want, save it. Now it's in the game. Teachers love creating shapes that match what they're teaching."

### "What age is this for?"
**Response**: "Ages 4-12 primarily, but we've seen everyone from preschoolers to adults enjoy it. Easy shapes for young kids, hard shapes for older ones, and custom creation for the advanced learners."

---

## 📊 Sales Talking Points

### Key Benefits

1. **Hands-On + Digital = Best of Both Worlds**
   - "Physical tangram play develops motor skills"
   - "Digital feedback provides instant encouragement"
   - "Kids aren't just staring at a screen"

2. **Easy for Teachers**
   - "No computer expertise needed"
   - "Works with standard tangram sets schools already have"
   - "Create puzzles in 2 minutes that match lesson plans"

3. **Flexible Deployment**
   - "Run from USB drive - no IT department needed"
   - "Or install properly with Start Menu shortcuts"
   - "Works offline - no internet required"

4. **Proven Educational Value**
   - "Develops spatial reasoning (critical for STEM)"
   - "Problem-solving and patience"
   - "Visual-spatial intelligence"
   - "Self-paced learning with immediate feedback"

### Price Positioning

**Individual/Home**: "Less than the cost of 3 educational apps, one-time purchase, unlimited use"

**School/Classroom**: "Cost per student is under [X] for entire year, reusable across grades"

**Enterprise/District**: "Bulk licensing available, includes support and custom shape library"

---

## ✅ Pre-Demo Checklist

**Day Before:**
- [ ] Charge laptop fully
- [ ] Test demo on laptop (full run-through)
- [ ] Load 3 USB drives with portable package
- [ ] Pack tangram pieces in protective case
- [ ] Pack backup webcam
- [ ] Print 10 quick reference cards
- [ ] Update installer link (verify it downloads)
- [ ] Prepare business cards with download link

**Day Of:**
- [ ] Arrive early to set up
- [ ] Test on venue's PC if using one
- [ ] Position camera for good lighting
- [ ] Run through demo once
- [ ] Have USB drives accessible
- [ ] Keep laptop charged

---

## 🎬 30-Second Elevator Pitch

> "Tangram Challenge combines traditional tangram puzzles with computer vision to create an engaging learning experience for kids. 
> 
> They play with real, physical puzzle pieces on a desk, while a camera tracks their progress and gives instant feedback on screen. 
>
> No complicated setup - just plug in a webcam and run. Teachers can create custom puzzles in minutes. 
>
> It develops spatial reasoning and problem-solving skills while keeping kids engaged with hands-on play instead of screen time.
>
> Want to see it in action?"

---

## 📞 Follow-Up Template

**Email after demo:**

```
Subject: Tangram Challenge Demo - Download Link

Hi [Name],

Great speaking with you at [event/call]! As promised, here's 
everything you need:

INSTANT DEMO (No Installation):
[Link to portable_package.zip]
Just unzip and double-click TangramLauncher.exe

PROFESSIONAL INSTALLER:
[Link to TangramChallenge_Setup.exe]  
Full installation with Start Menu integration

DOCUMENTATION:
- Quick Start Guide: [link]
- Video Demo: [link if available]
- Pricing Sheet: [link]

Try it with your [students/kids/team] and let me know what you 
think! I'm happy to schedule a call to discuss implementation.

Best regards,
[Your name]
```

---

## 🎯 Success Metrics

Track these for each demo:

- [ ] Demo completed without technical issues
- [ ] Customer understood value proposition
- [ ] Left customer with materials (USB/link/card)
- [ ] Scheduled follow-up call/meeting
- [ ] Customer showed interest in pricing

**Good Demo Signs:**
- Customer asks "How much?"
- Customer asks "Can we customize X?"
- Customer wants to demo it to colleagues
- Customer asks about support/training

---

## 🚨 Troubleshooting On-Site

### Launcher won't start
1. Right-click → Run as Administrator
2. Check antivirus didn't block it
3. Try from different folder (not Downloads)

### Camera not detected
1. Verify camera is plugged in
2. Close Skype/Teams/other camera apps
3. Try "Test Camera" button
4. Use backup webcam from your bag

### Pieces not detected
1. Click "Calibrate Camera"
2. Improve lighting (move desk lamp)
3. Use lighter desk surface (put paper down)
4. Make sure pieces are the right colors

### Game runs slowly
1. Close other applications
2. Reduce screen resolution
3. Use newer computer if available

---

## 💡 Pro Tips

1. **Always have backup USB** - demo PCs can be finicky
2. **Bring your own webcam** - don't rely on built-in cameras
3. **Practice the 2-minute demo** - keep it snappy
4. **Let THEM move pieces** - engagement goes way up
5. **Show shape editor** - this always impresses teachers
6. **Have tangram pieces visible** - people are drawn to colorful objects
7. **Mention it works offline** - schools love this
8. **Emphasize "no screen time"** - parents love this

---

## 📦 What to Bring

**Essential:**
- [ ] Laptop with game installed
- [ ] 3+ USB drives (portable package)
- [ ] Tangram pieces (7 colors)
- [ ] USB webcam (backup)
- [ ] Power cable for laptop

**Nice to Have:**
- [ ] Quick reference cards (printed)
- [ ] Lightweight desk lamp (for lighting)
- [ ] White poster board (for desk surface)
- [ ] Business cards with download link
- [ ] Camera stand/tripod

**Digital:**
- [ ] Installer link (in cloud)
- [ ] Demo video (on phone)
- [ ] Pricing sheet (PDF)
- [ ] Customer list for follow-up

---

**You're ready to close deals! 🎉**

Questions? See DEPLOYMENT_GUIDE.md for technical details.
