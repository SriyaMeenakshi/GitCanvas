# GitCanvas Exploration Findings

## 1. Main Purpose
GitCanvas is a "Profile Architect" for GitHub. It allows users to generate various stats cards, charts, and visual elements to enhance their GitHub profile READMEs.

## 2. Input Fields
### Identify (Sidebar)
- **GitHub Username:** Text input (default: torvalds).
### Global Style (Sidebar)
- **Select Theme:** Dropdown (Default, etc.).
- **Customize Colors (Collapsible):** Color pickers for Bg Color, Title Color, Text Color, Icon Color.
- **Custom Theme Creator (Collapsible):** 
    - Theme Name (Text input)
    - Bg Color, Border Color, Text Color, Icon Color (Color pickers).
### Settings (Sidebar)
- **GitHub Token:** Password input for personal access token.
- **Enable Animations:** Checkbox.
- **Output Format:** Radio buttons (Markdown, HTML).
- **Refresh Data:** Button.

## 3. Output Types (Tabs)
1.  **Main Stats:** Stars, Commits, Repos, Followers. Checkboxes to toggle each.
2.  **Languages:** Top languages horizontal bar chart. Exclude languages option.
3.  **Top Repositories:** Most starred/active repos. Sort by options and count slider.
4.  **Contributions:** GitHub-style contribution heat map. Date range selection.
5.  **GitHub Streak:** Current/longest streak and total contributions card.
6.  **Social Links:** Badge-style links for Twitter, LinkedIn, etc.
7.  **Icons & Badges:** Tech stack icons (Language, Frontend, Backend, etc.). Style selection (flat, for-the-badge).
8.  **AI Roast:** Generates a humorous roast of the GitHub profile.
9.  **Recent Activity:** Displays latest PRs or Issues.
10. **Visual Elements:** Add Emojis, GIFs, or Stickers to a 'Canvas'.
11. **Trophy:** Achievements as a 'Trophy' card with quality tiers (e.g., Legend Tier).

## 4. Visual Style & Color Scheme
- **Layout:** Streamlit sidebar + main tabbed interface.
- **Color Scheme:** Dark mode cards by default (Dark grey backgrounds, bright blue/white text). Sidebar is Streamlit's default light/dark based on user system.
- **Icons:** Uses Material/Google icons for sidebar labels and tabs.

## 5. User Flow
1.  Enter GitHub Username in the sidebar.
2.  Select a theme or customize colors.
3.  Navigate through tabs to select the desired card/visual.
4.  Adjust tab-specific settings (e.g., exclude languages, select platforms).
5.  Preview the generated card in the main area.
6.  Copy the generated Markdown/HTML code from the "Integration" section.
7.  Optionally download the result as SVG, PNG, or JPEG.

## 6. API Integrations
- **GitHub API:** Fetches user stats, repos, and activity.
- **Custom API:** Integration codes point to `https://gitcanvas-api.vercel.app/`.
- **AI Integration:** For the 'AI Roast' feature.
