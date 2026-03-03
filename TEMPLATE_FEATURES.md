# Template Features Overview

This document provides a visual description of all the templates included in the project.

## 🏠 Home Page (home.html)

**URL:** `/`

### Features:
- **Hero Section**
  - Large gradient background (purple to violet)
  - Welcome headline and subtext
  - Call-to-action buttons
  - Smooth fade-in animations

- **Features Section**
  - 4 feature cards with gradient icons
  - Icons: Rocket, Shield, Cogs, Users
  - Hover effects (cards lift up)
  - Descriptions of key features

- **Call-to-Action Section**
  - Bottom banner with gradient background
  - "Ready to Get Started?" heading
  - Registration button

### Visual Style:
- Gradient background: Linear purple gradient
- White content cards
- Rounded corners (20px)
- Box shadows for depth
- Responsive grid layout

---

## 🔐 Login Page (login.html)

**URL:** `/login/`

### Features:
- **Login Card**
  - Gradient header with lock icon
  - Email input field
  - Password input with show/hide toggle
  - "Remember me" checkbox
  - "Forgot password?" link
  - Social login buttons (Google, GitHub)

- **Interactive Elements**
  - Eye icon toggles password visibility
  - Form validation on submit
  - Error messages display
  - Auto-focus on email field

- **Design Elements**
  - Slide-up animation on load
  - Purple gradient header
  - White card body
  - Rounded inputs
  - Hover effects on buttons

### Form Fields:
1. Email (required)
2. Password (required, with toggle)
3. Remember Me (optional checkbox)

---

## ✍️ Registration Page (register.html)

**URL:** `/register/`

### Features:
- **Registration Card**
  - Gradient header with user-plus icon
  - First and Last name fields (2-column layout)
  - Email field
  - Password with strength indicator
  - Confirm password field
  - Terms & conditions checkbox

- **Password Strength Indicator**
  - Visual bar that changes color
  - Red (weak) → Yellow (medium) → Green (strong)
  - Real-time updates as user types
  - Based on length, complexity, special chars

- **Validation**
  - Email format validation
  - Password match checking
  - Duplicate email detection
  - Required field indicators

### Form Fields:
1. First Name (optional)
2. Last Name (optional)
3. Email (required, validated)
4. Password (required, with strength meter)
5. Confirm Password (required, must match)
6. Terms Agreement (required checkbox)

---

## 📊 Dashboard Page (dashboard.html)

**URL:** `/dashboard/` (login required)

### Features:
- **Welcome Section**
  - Personalized greeting with user's name
  - "Edit Profile" button
  - White card with shadow

- **Statistics Cards (4 cards)**
  - Total Tasks (purple gradient icon)
  - Completed (green gradient icon)
  - Pending (orange gradient icon)
  - Progress (blue gradient icon)
  - Each card shows number and label
  - Hover effect: lift up

- **Recent Activity Section**
  - Timeline of recent actions
  - Each item has:
    - Colored icon circle
    - Activity title
    - Timestamp
  - Activities:
    - Document uploaded (blue)
    - Task completed (green)
    - Team member added (yellow)
    - New comments (pink)
    - System update (indigo)

- **Quick Actions Panel**
  - 4 action buttons:
    - Create New Task
    - Upload File
    - Invite Team
    - Settings
  - Icon + text layout
  - Hover effect: purple background

- **Project Progress Panel**
  - Progress bars for different projects
  - Each bar shows:
    - Project name
    - Percentage
    - Colored progress bar
  - Projects tracked:
    - Frontend Development (85%)
    - Backend API (70%)
    - Database Design (95%)
    - Testing (45%)

### Layout:
- 8-column main content (left)
- 4-column sidebar (right)
- Responsive: stacks on mobile

---

## 👤 Profile Page (profile.html)

**URL:** `/profile/` (login required)

### Features:
- **Profile Header**
  - Large circular avatar
  - Shows profile picture or user's initials
  - Full name display
  - Email address
  - Status badges (Admin, Active)

- **Tabbed Interface**
  
  **Tab 1: Overview**
  - Display user information:
    - Full Name
    - Email
    - Phone Number
    - Birth Date
    - Bio
    - Member Since
  - Read-only view

  **Tab 2: Edit Profile**
  - Editable form with fields:
    - First Name
    - Last Name
    - Email (disabled/read-only)
    - Phone Number
    - Birth Date (date picker)
    - Bio (textarea)
    - Profile Picture (file upload)
  - "Save Changes" button

  **Tab 3: Security**
  - Password change form:
    - Current Password
    - New Password
    - Confirm New Password
  - "Change Password" button
  - Two-Factor Authentication section
  - "Enable 2FA" button

- **Sidebar**
  
  **Account Stats Card:**
  - Total Tasks (with icon)
  - Documents (with icon)
  - Team Members (with icon)
  - Points (with icon)

  **Quick Links Card:**
  - Dashboard button
  - Settings button
  - Help Center button
  - Logout button (red)

### Visual Elements:
- Circular avatar with gradient background
- Colored badges
- Underlined tab navigation
- Icon indicators throughout
- Responsive 2-column layout

---

## 🎨 Design System

### Color Palette:
- **Primary:** #4f46e5 (Indigo)
- **Secondary:** #7c3aed (Purple)
- **Success:** #10b981 (Green)
- **Warning:** #f59e0b (Amber)
- **Danger:** #ef4444 (Red)
- **Info:** #3b82f6 (Blue)
- **Dark:** #1f2937 (Gray-800)
- **Light:** #f9fafb (Gray-50)

### Typography:
- Font Family: 'Segoe UI', system fonts
- Headings: Bold (700 weight)
- Body: Regular (400 weight)
- Labels: Semi-bold (600 weight)

### Spacing:
- Card padding: 30-40px
- Section margins: 30px
- Input padding: 12-15px
- Button padding: 10-25px

### Border Radius:
- Cards: 15-20px
- Buttons: 10px
- Inputs: 10px
- Icons: 10-15px
- Avatars: 50% (circular)

### Shadows:
- Cards: 0 10px 30px rgba(0,0,0,0.1)
- Hover: 0 15px 35px rgba(0,0,0,0.15)
- Buttons: 0 10px 20px with primary color

### Animations:
- Slide up on load: 0.5s ease-out
- Hover lift: transform translateY(-5px)
- Fade in: opacity 0 to 1
- Smooth transitions: 0.3s

---

## 📱 Responsive Breakpoints

### Mobile (< 768px)
- Single column layout
- Stacked cards
- Collapsed navigation (hamburger menu)
- Full-width buttons

### Tablet (768px - 1024px)
- 2-column grid for stats
- Sidebar below main content
- Adjusted spacing

### Desktop (> 1024px)
- Multi-column layouts
- Sidebar alongside content
- Larger typography
- More whitespace

---

## 🔔 Interactive Features

### Form Validation:
- Real-time field validation
- Error messages below fields
- Success states (green border)
- Error states (red border)

### Password Features:
- Show/hide toggle (eye icon)
- Strength indicator bar
- Match validation
- Complexity requirements

### Navigation:
- Active page highlighting
- Hover effects
- Mobile menu toggle
- Dropdown support

### Alerts/Messages:
- Auto-dismissible alerts
- Color-coded by type
- Fade-in animation
- Close button

---

## 🎯 User Experience (UX)

### Accessibility:
- Semantic HTML5 elements
- ARIA labels where needed
- Keyboard navigation support
- Focus indicators
- Screen reader friendly

### Performance:
- CDN for libraries (Bootstrap, Font Awesome)
- Minimal custom CSS
- Optimized animations
- Fast page loads

### Usability:
- Clear call-to-action buttons
- Intuitive navigation
- Helpful placeholder text
- Visual feedback on interactions
- Consistent layout patterns

---

## 🚀 Getting Started

1. **First Time Users:**
   - Visit home page → Click "Get Started"
   - Fill registration form
   - Login automatically after signup
   - See dashboard

2. **Returning Users:**
   - Click "Sign In"
   - Enter credentials
   - Check "Remember Me" for convenience
   - Access dashboard

3. **Profile Management:**
   - Click profile icon in nav
   - View current info in Overview tab
   - Edit info in Edit Profile tab
   - Change password in Security tab

4. **Navigation Flow:**
   ```
   Home → Login/Register → Dashboard → Profile
                ↓              ↓          ↓
              Logout      Quick Actions  Settings
   ```

---

## 💡 Customization Tips

### Change Brand Colors:
Edit CSS variables in `base.html`:
```css
--primary-color: #YOUR_COLOR;
```

### Add New Page:
1. Create template in `templates/`
2. Create view in `template_views.py`
3. Add URL in `template_urls.py`
4. Add navigation link in `base.html`

### Modify Layout:
- Adjust grid columns (col-md-X)
- Change spacing (mb-X, mt-X, p-X)
- Update border radius
- Modify box shadows

### Add Features:
- Use Bootstrap components
- Add Font Awesome icons
- Include custom JavaScript
- Extend base template

---

For implementation details, see **TEMPLATES_GUIDE.md**
