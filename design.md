# Flashoot – Complete Design Document

---

## 1. Brand Identity

| Property | Value |
|---|---|
| **Brand Name** | FLASHOOT |
| **Logo Style** | Wordmark — "FLA" + lightning bolt icon replacing "SH" + "OOT" |
| **Logo Color** | White wordmark on dark background; Red lightning bolt accent |
| **Brand Tone** | Bold, fast, energetic, professional, tech-forward |
| **Target Audience** | Content creators, businesses, wedding clients, social media brands |
| **Core Tagline** | *"We Shoot + Edit + Deliver Reels in 10 Minutes"* |
| **Sub-tagline** | *"Not Just Instant Delivery, But…"* |

---

## 2. Color Palette

| Name | Hex / Description | Usage |
|---|---|---|
| **Primary Background** | `#0D0000` – Near-black deep red/maroon | Full page background |
| **Secondary Background** | `#1A0000` – Very dark crimson | Cards, section backgrounds |
| **Card Background** | `#1C0505` – Dark wine red | Pricing cards, feature boxes |
| **Primary Accent** | `#E8001C` / `#CC0000` – Vivid red | CTA buttons, highlights, badge labels, icons |
| **Secondary Accent** | `#FF2200` – Bright orange-red | Hover states, lightning bolt icon |
| **Primary Text** | `#FFFFFF` – Pure white | Headings, card titles, body text on dark bg |
| **Secondary Text** | `#CCCCCC` / `#AAAAAA` – Light gray | Subheadings, descriptions, bullet lists |
| **Muted Text** | `#888888` – Mid gray | Meta info, timestamps, fine print |
| **Gold / Premium Accent** | `#C8A95A` / `#D4A843` – Warm gold | "Luxe" section, premium tier labels |
| **Border / Divider** | `rgba(255,255,255,0.08)` – Subtle white | Card borders, section separators |
| **Overlay** | `rgba(0,0,0,0.5)` | Image overlays, modal backgrounds |

---

## 3. Typography

| Element | Font Family | Weight | Size (approx) | Style |
|---|---|---|---|---|
| **Hero Headline** | Bold sans-serif (likely Poppins or Montserrat) | 900 / Black | ~56–72px | Uppercase, tight tracking |
| **"10 Minutes"** | Display / Black weight | 900 | ~80–100px | Dominant, hero text, white |
| **Section Headings** | Bold sans-serif | 700 | ~28–36px | White, centered |
| **Card Titles** | Semi-bold sans-serif | 600 | ~18–22px | White |
| **Body Text** | Regular sans-serif | 400 | ~14–16px | Light gray |
| **Price Labels** | Bold / Black | 700–900 | ~24–36px | White, ₹ prefix |
| **Button Text** | Semi-bold | 600 | ~14–16px | Uppercase or Title Case |
| **Badge / Tag Text** | Bold | 700 | ~10–12px | All caps |
| **Footer Text** | Regular | 400 | ~12–13px | Gray |

> **Typography Note:** The overall typeface system is a geometric sans-serif (very likely **Poppins** or **Montserrat**), consistent across all weights. Number displays are in the heaviest available weight to maximize visual punch.

---

## 4. Layout & Grid

| Property | Value |
|---|---|
| **Max Content Width** | ~1200px centered |
| **Page Layout** | Single-column, vertically stacked sections |
| **Section Padding** | ~60–100px top/bottom |
| **Card Grid** | 2–3 column CSS grid on desktop |
| **Gutters** | ~20–24px between grid items |
| **Mobile Breakpoint** | ~768px (stacks to single column) |
| **Navbar Height** | ~56–64px |
| **Border Radius (Cards)** | ~12–16px |
| **Border Radius (Buttons)** | ~8px (slightly rounded) |

---

## 5. Navigation Bar

- **Position:** Fixed top, full width
- **Background:** Solid black / near-black (`#0A0000`)
- **Left:** FLASHOOT wordmark/logo (white + red bolt)
- **Center:** Navigation links (white text, small size)
- **Right:** CTA button — "Sign Up" or "Get Started" in red (`#CC0000`) with white text
- **Height:** ~56px
- **Border Bottom:** Subtle dark red or transparent
- **Font Size:** ~14px for nav links

---

## 6. Hero Section

### Layout
- Full-width, dark background with subtle texture or radial gradient centered
- Centered text alignment

### Content (top to bottom)
1. **Top Tag Line:** Small label — *"We Shoot + Edit + Deliver Reels in"* (white, regular weight, ~18px)
2. **Hero Number:** `10 Minutes` — massive, white, Black weight (~80–100px), dominant visual
3. **Sub-description:** Short paragraph in gray, ~16px, centered
4. **Phone Mockup:** Centered image of a smartphone showing the Flashoot app interface (dark UI with red accents, video reel feed visible)
5. **App Store Badges:** Row of 3 badges — App Store, Google Play, Get Started (Web) — white outlined pill-shaped badges with icons
6. **CTA Buttons Row:**
   - **"Book Now"** — Filled red button (`#CC0000`), white text, ~14px, rounded corners
   - **"Become a Partner"** — Outlined button, white border, white text
7. **Social Proof Strip:**
   - `50,000+` Shoots | `4.19` Rating (stars) | `500+` Cities
   - Small gray label text under each number
8. **Press Logos Row:** Logos of OutlookIndia, Inc42 Magazine, YourStory, Flashoot (white/gray, small)

---

## 7. "Not Just Instant Delivery, But…" Section

- **Background:** Same deep dark red/maroon
- **Heading:** *"Not Just Instant Delivery, But…"* — centered, white, ~28px bold
- **"My Shoots" Badge:** Small pill badge, red background, above heading
- **Two Feature Cards (side by side):**

### Card 1: Talented Professional Makers
  - Black card with dark red tint
  - Icon/image area: Stylized image of a videographer/camera operator
  - Title: "Talented Professional Makers" — white, bold
  - Description: Gray body text, ~14px

### Card 2: Easy Booking
  - Same card style
  - Icon/image: Phone or booking UI illustration
  - Title: "Easy Booking" — white, bold
  - Description: Gray body text, ~14px

---

## 8. Bestsellers / Pricing Section

- **Section Label:** Small red pill badge — "Bestsellers" centered above
- **Section Heading:** `Bestsellers` — large, white, centered
- **Layout:** 2 pricing cards side by side (Hourly Plan, Half-Day Plan), possibly a third

### Pricing Card Design (each card):
| Property | Value |
|---|---|
| Background | Dark red/maroon (`#1C0505`) |
| Border | Subtle red or dark border |
| Border Radius | ~12–16px |
| Shadow | Dark diffuse shadow |
| Padding | ~24–32px |

### Card 1: Hourly Plan
- **Title:** "Hourly Plan" — white, bold, ~20px
- **Price:** `₹1,999` — large, white/bold, ~32px; smaller gray text for duration
- **Feature List:** Bulleted list, gray text, checkmarks in red or white
- **CTA Button:** "Book Now" — red filled, full-width within card
- **Tag:** Optional "Popular" badge

### Card 2: Half-Day Plan
- **Title:** "Half-Day Plan"
- **Price:** `₹4,999` — large, bold
- **Feature List:** Bulleted, gray
- **CTA Button:** "Book Now" — red filled

> Cards have consistent padding, border radius, and shadow. Selected/highlighted card may have a brighter red border or glow.

---

## 9. "Features That Make Us Stand Out" Section

- **Heading:** `Features That Make Us Stand Out` — white, bold, centered
- **Badge:** Small red pill label above heading
- **Layout:** App screenshot (phone mockup) on left; feature list / carousel dots on right
- **Phone Mockup:** Shows dark red UI of Flashoot app with video/reel content
- **Feature Carousel:** Dot indicators at bottom suggesting multiple slides
- **Feature Items (visible):**
  - Text descriptions with icons
  - Gray body text, white titles
- **Background:** Slightly lighter dark red, or same as page

---

## 10. "Choose Your Perfect Plan" Section

- **Heading:** `Choose Your Perfect Plan` — white, bold, centered
- **Sub-heading:** Small gray descriptor text below heading
- **Badge:** Small red pill at top

### Sub-section A: Wedding Packages

| Property | Detail |
|---|---|
| Left Column | Wedding Packages heading, pricing from `₹14,999` (large, bold, white) |
| Plan Tiers | Silver, Gold, Platinum — pill/tab selector buttons |
| Active Tier | Red background pill |
| Inactive Tier | Dark/outlined pill |
| CTA | "Book Now" — red button |
| Description | Gray body text for each plan |

### Sub-section B: Business

- Similar card layout for Business plans
- **Customized Pricing** prominently displayed
- "Get a Quote" CTA button
- Feature list in gray text

---

## 11. Luxe Section

- **Full-width section** with slightly different dark background (darker or subtle texture)
- **Logo:** `FLASHOOT LUXE` — white wordmark, larger, centered; "LUXE" in gold/yellow italic
- **Price:** `₹1,99,999` — very large, bold, white, centered; small label below
- **Description:** Gray paragraph text, centered
- **CTA Button:** Red "Book Now" — centered
- **Visual Style:** Premium, minimal; gold accents distinguish from standard sections

---

## 12. "What Our Loving Customers Say" Section (Testimonials)

- **Heading:** `What Our Loving Customers Say` — white, bold, centered
- **Layout:** Horizontal scroll or carousel of testimonial cards
- **Carousel Dots:** White dot indicators at bottom

### Testimonial Card Design:
| Property | Value |
|---|---|
| Background | Dark card (`#1A0000` or `#1C0505`) |
| Border Radius | ~12px |
| Padding | ~20–24px |
| Avatar | Circular profile photo, ~40px |
| Name | White, bold, ~14px |
| Review Text | Gray, ~13–14px, 3–5 lines |
| Stars | Red/yellow star rating icons |

- Visible cards include user names: "Ankur Gadgil", "Ananya Pandey"

---

## 13. FAQ Section

- **Heading:** `Got Questions?` — white, bold, centered
- **Sub-heading:** Small gray text below
- **Badge:** Red pill label above heading
- **Layout:** Accordion/expandable FAQ list
- **FAQ Item Style:**
  - Dark card background
  - White question text (~15px, semi-bold)
  - Gray answer text (revealed on expand)
  - Plus/minus icon or chevron on right
  - Bottom border divider between items
- **Visible FAQ:** "What exactly is Flashoot?" shown as first question

---

## 14. App Download Section

- **Heading:** `Download The Fastest App Now` — white, bold, centered
- **Sub-heading:** Gray text with app description
- **Left Column:**
  - "Get Upto 50% Discount" — red badge/tag
  - "Get The App" heading
  - App Store badge (white outlined, ~140px wide)
  - Google Play badge (white outlined, ~140px wide)
- **Right Column:**
  - 2–3 phone mockups showing the Flashoot app UI (dark red design with reels)
  - Mockups slightly overlapping or stacked for depth
- **Background:** Same deep dark maroon

---

## 15. Floating Chat Widget

- **Position:** Fixed, bottom-right corner
- **Appearance:** Red circular button with chat/message icon (white)
- **Label:** Small tooltip or label "Hi there 👋" popup card with brief text
- **Shadow:** Soft red glow or dark shadow

---

## 16. Footer

- **Background:** Same dark maroon as page (`#0D0000`)
- **Top Border:** Subtle red or dark divider line
- **Layout:** Multi-column grid
  - Column 1: FLASHOOT logo + short brand description
  - Column 2: Links (Company, About, Careers, etc.)
  - Column 3: Links (Services, Pricing, etc.)
  - Column 4: Contact / Social icons
- **Social Icons:** Small circular icons (Instagram, YouTube, LinkedIn, etc.) in white or gray
- **Bottom Bar:**
  - Copyright text: "© 2024 Flashoot. All rights reserved."
  - Partner/certification logos: DPIIT, Startup India badge (white)
  - Privacy Policy, Terms of Service links — gray, ~12px

---

## 17. Buttons

| Type | Style |
|---|---|
| **Primary / CTA** | Filled red (`#CC0000`), white text, ~14px semi-bold, 8px border-radius, ~44px height |
| **Secondary / Outline** | White border, white text, transparent background, same radius |
| **Plan Tier Selector (Active)** | Red background pill, white text, ~12px |
| **Plan Tier Selector (Inactive)** | Dark outlined pill, gray text |
| **App Badge** | Black background, white icon + text, rounded rectangle, ~140×44px |

---

## 18. Badges & Tags

| Style | Usage |
|---|---|
| Red filled pill | Section labels (Bestsellers, My Shoots, etc.) |
| White outlined pill | App download badges |
| Gold/yellow text | Luxe section label |
| Star ratings | Testimonials, hero stats |

---

## 19. Cards

| Property | Value |
|---|---|
| Background | `#1A0000` to `#1C0505` (dark wine red) |
| Border | 1px solid `rgba(255,50,50,0.15)` |
| Border Radius | 12–16px |
| Padding | 24–32px |
| Shadow | `0 8px 32px rgba(0,0,0,0.4)` |
| Hover Effect | Subtle border glow, slight scale (transform: scale 1.02) |

---

## 20. Iconography

- **Style:** Flat, minimal, line icons or filled icons
- **Color:** White or red
- **Usage:** Feature bullets, app badges, social links, FAQ chevrons
- **Lightning Bolt:** Brand icon — stylized, red/orange, used in logo

---

## 21. Imagery & Media

| Element | Description |
|---|---|
| Phone Mockups | Dark-themed Flashoot app screenshots, 2–3 devices shown |
| People / Creator Photos | High-contrast editorial photos on dark backgrounds |
| App UI Screenshots | Dark red interface with reel thumbnails, red accents |
| Press Logos | White/gray monochrome versions of media brand logos |
| Partner Logos | DPIIT, Startup India — white monochrome in footer |

---

## 22. Spacing System

| Token | Value |
|---|---|
| `--space-xs` | 4px |
| `--space-sm` | 8px |
| `--space-md` | 16px |
| `--space-lg` | 24px |
| `--space-xl` | 40px |
| `--space-2xl` | 64px |
| `--space-3xl` | 96px |

---

## 23. Motion & Interactions

| Element | Animation |
|---|---|
| Hero text | Fade-in + slide-up on load |
| Pricing cards | Scale-up on hover |
| CTA buttons | Brightness increase + slight scale on hover |
| Accordion FAQ | Smooth height expand/collapse |
| Carousel | Horizontal slide with dot indicator update |
| App badge hover | Subtle lift shadow |
| Chat widget | Bounce entry animation, pulse on idle |

---

## 24. Responsive Behavior

| Breakpoint | Behavior |
|---|---|
| Desktop (>1024px) | 2–3 column grids, full nav, large hero text |
| Tablet (768–1024px) | 2-column grids, compressed nav |
| Mobile (<768px) | Single column, hamburger menu, stacked sections, smaller type |

---

## 25. Section Order (Top to Bottom)

1. Navigation Bar (Fixed)
2. Hero Section
3. Social Proof Strip + Press Logos
4. "Not Just Instant Delivery" Features
5. Bestsellers / Pricing Cards
6. Features That Make Us Stand Out
7. Choose Your Perfect Plan (Wedding + Business)
8. Luxe Section
9. Testimonials / Reviews
10. FAQ Section
11. App Download CTA
12. Footer
13. Floating Chat Widget (Overlay)