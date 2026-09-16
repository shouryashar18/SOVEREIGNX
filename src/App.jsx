import {
  HashRouter,
  Routes,
  Route,
  Link,
  Navigate,
  useParams,
} from "react-router-dom";

import { pages } from "./pages.js";
import "./App.css";

import { useEffect } from "react";
import { testBackend } from "./api.js";


function groupPages() {
  const groups = {};

  for (const p of pages) {
    if (!groups[p.group]) groups[p.group] = [];
    groups[p.group].push(p);
  }

  return groups;
}


function Sidebar() {
  const groups = groupPages();

  return (
    <nav className="sidebar">

      <Link to="/" className="brand">
        SIH26171 <span>Screens</span>
      </Link>

      <Link
        to="/gallery"
        className="nav-link"
        style={{
          marginBottom: "1rem",
          display: "block",
        }}
      >
        ⊞ All Screens (gallery)
      </Link>

      {Object.entries(groups).map(([group, items]) => (
        <div key={group} className="nav-group">

          <div className="nav-group-label">
            {group}
          </div>

          {items.map((p) => (
            <Link
              key={p.slug}
              to={`/screen/${p.slug}`}
              className="nav-link"
            >
              {p.title}
            </Link>
          ))}

        </div>
      ))}

    </nav>
  );
}


function Home() {
  return (
    <div className="home">

      <h1>All Screens</h1>

      <p className="subtitle">
        22 screens exported from Stitch, wired into one app. Click any card to
        open it — each keeps its own original styling.
      </p>

      <div className="grid">

        {pages.map((p) => (
          <Link
            key={p.slug}
            to={`/screen/${p.slug}`}
            className="card"
          >

            <div className="card-thumb">

              <img
                src={`/pages/${p.slug}/screen.png`}
                alt={p.title}
                loading="lazy"
                onError={(e) => {
                  e.currentTarget.style.display = "none";
                }}
              />

            </div>

            <div className="card-title">
              {p.title}
            </div>

          </Link>
        ))}

      </div>

    </div>
  );
}


function Screen() {

  const { slug } = useParams();

  const page = pages.find(
    (p) => p.slug === slug
  );

  return (
    <div className="screen-viewer">

      <div className="screen-header">

        <Link
          to="/"
          className="back-link"
        >
          ← All screens
        </Link>

        <span className="screen-title">
          {page ? page.title : slug}
        </span>

        <a
          href={`/pages/${slug}/index.html`}
          target="_blank"
          rel="noreferrer"
          className="open-tab-link"
        >
          Open in new tab ↗
        </a>

      </div>

      <iframe
        title={slug}
        src={`/pages/${slug}/index.html`}
        className="screen-frame"
      />

    </div>
  );
}


export default function App() {

  // Test backend connection
  useEffect(() => {

    testBackend()
      .then((data) => {

        console.log(
          "Backend connected:",
          data
        );

      })
      .catch((error) => {

        console.error(
          "Backend connection error:",
          error
        );

      });

  }, []);


  return (
    <HashRouter>

      <div className="app-shell">

        <Sidebar />

        <main className="main-panel">

          <Routes>

            <Route
              path="/"
              element={
                <Navigate
                  to="/screen/sovereignx_landing_page_deep_obsidian_v2"
                  replace
                />
              }
            />

            <Route
              path="/gallery"
              element={<Home />}
            />

            <Route
              path="/screen/:slug"
              element={<Screen />}
            />

          </Routes>

        </main>

      </div>

    </HashRouter>
  );
}