# IPTVking Design Guidelines

## Design Approach
**Reference-Based:** Drawing inspiration from leading streaming platforms (Netflix, YouTube TV, Spotify) with emphasis on immersive content presentation and seamless media consumption. Dark-first interface optimized for video playback environments.

## Core Design Principles
1. **Content-First:** Visual media (channel logos, posters, backdrops) drives the hierarchy
2. **Immersive Darkness:** Deep backgrounds that don't compete with video content
3. **Effortless Discovery:** Prominent search, intuitive filtering, visual browsing
4. **Multi-Context Flexibility:** Seamless experience across single and multi-view modes

---

## Typography

**Font Stack:**
- **Primary:** Inter (Google Fonts) - UI text, buttons, labels
- **Display:** Bebas Neue - Section headers, channel names
- **Mono:** JetBrains Mono - Technical info (bitrate, stats)

**Hierarchy:**
- Hero Titles: 48-64px, bold, Bebas Neue
- Section Headers: 24-32px, semibold, Inter
- Channel Names: 16-18px, medium, Inter
- Body Text: 14-16px, regular, Inter
- Metadata/Stats: 12-14px, regular, JetBrains Mono

---

## Layout System

**Spacing Primitives:** Tailwind units of **2, 4, 8, 12** (p-2, m-4, gap-8, py-12)

**Grid Systems:**
- Channel Browser: 4-6 columns on desktop (grid-cols-4 lg:grid-cols-6)
- EPG Grid: Responsive time-slot columns with fixed channel sidebar
- Featured Content: 2-3 columns for poster cards
- Multi-View: 2x2 grid for quad-view, flexible for 1-3 streams

**Container Strategy:**
- App Shell: Full viewport with fixed header/sidebar
- Content Areas: max-w-7xl with px-8 padding
- Player Zone: Full-width, aspect-ratio locked containers

---

## Component Library

### Navigation
**Top Navigation Bar:**
- Fixed header with app logo/branding
- Global search bar (prominent, centered or right-aligned)
- User profile/settings icon
- System stats display (CPU, memory, bitrate) in minimal badges

**Sidebar (Desktop):**
- Collapsible channel category navigation
- Favorites quick access
- Playlist switcher
- Recording scheduler link

### Channel Browser
**Channel Cards:**
- Square aspect ratio with channel logo/poster
- Hover: Scale transform (1.05), elevated shadow
- Channel name overlay on gradient backdrop
- Current program indicator (small badge/pill)
- Grid layout with consistent gaps (gap-4)

### EPG Grid
**Time-Grid Interface:**
- Sticky header row (time slots in 30min increments)
- Sticky left column (channel names/logos)
- Program cells span based on duration
- Current time indicator (vertical line or highlighted column)
- Active program: Subtle highlight or border accent
- Currently playing channel row: Distinct visual treatment

### Video Player
**Single-View Player:**
- 16:9 aspect ratio container
- Overlay controls (bottom gradient fade)
- Play/pause, volume, fullscreen, quality selector
- Progress bar with seek preview thumbnails
- Channel info overlay (top-left): Logo, name, current program

**Multi-View Grid:**
- Equal-sized player containers in 2x2 layout
- Synchronized playback controls toggle
- Active player border highlight
- Individual mute/volume controls per stream
- Minimize/maximize individual streams

### Content Cards
**Movie/Show Metadata Cards:**
- Poster image (2:3 aspect ratio)
- Title, release date, rating display
- Truncated overview text (2-3 lines)
- Play/Record/Add to Favorites action buttons
- Hover: Backdrop preview expansion

### Forms & Inputs
**Search Bar:**
- Rounded corners (rounded-lg)
- Icon prefix (magnifying glass)
- Autocomplete dropdown with channel suggestions
- Dark background with subtle border

**Playlist Upload:**
- Drag-and-drop zone with dashed border
- File browser button
- Progress bar during parsing
- Chunked loading feedback (e.g., "Loading channels 1-1500...")

### Overlays & Modals
**Recording Scheduler:**
- Modal with dark backdrop blur
- Program details with poster/backdrop
- Date/time picker
- Recurring options (daily, weekly)
- Storage location selector

**Settings Panel:**
- Slide-out drawer from right
- Tabbed sections (General, Playback, EPG, API Keys)
- Toggle switches for features
- Theme selector (though defaults to dark)

### System Monitoring
**Resource Stats Display:**
- Compact pills/badges in header
- Real-time updates (1-2s refresh)
- Visual indicators: Green (good), Yellow (moderate), Red (high usage)
- Format: "CPU: 45% | Mem: 60% | ↓ 2.5 MB/s"

---

## Images

**Hero Section:**
- Full-width backdrop image from TMDB (featured content or trending channel)
- Gradient overlay (bottom to top, black to transparent)
- Centered content: Featured program title, description, Play CTA
- Buttons on blur background (backdrop-blur-sm bg-white/20)

**Channel Logos:**
- Fetched from channel metadata or placeholder
- Displayed in cards and EPG sidebar
- Square format, centered within container

**Posters & Backdrops:**
- TMDB integration for movies/shows
- Posters: 2:3 ratio for card grids
- Backdrops: 16:9 for hero/detail views
- Lazy loading for performance

---

## Animations
Use sparingly for polish, not distraction:
- Card hover transforms (scale, shadow)
- Smooth transitions on player controls (opacity, transform)
- EPG scroll with smooth-scroll behavior
- Modal/drawer open/close (slide, fade)
- Avoid auto-playing carousels or excessive motion

---

## Key Sections

**Home/Dashboard:**
- Hero with featured content (backdrop image, title, CTA)
- Continue Watching row (horizontal scroll cards)
- Favorites section (grid or horizontal scroll)
- Categories/Genres (collapsible rows with channel cards)

**Live Channels:**
- Grid view of all channels with logos
- Search and category filters (sidebar or top bar)
- Sort options (alphabetical, recently watched)

**EPG Guide:**
- Full-screen time-grid interface
- Search for programs or channels
- Highlight current time and active channel
- Click program to view details or schedule recording

**Multi-View Player:**
- 2x2 grid layout for quad-view
- Synchronized playback toggle
- Individual stream controls
- Quick channel switcher per player

**Recordings:**
- List or grid view of scheduled/completed recordings
- Status indicators (scheduled, in-progress, completed)
- Storage usage display