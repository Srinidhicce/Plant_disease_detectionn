import React from "react";
import Navbar from "./Navbar";
import UploadImage from "./UploadImage";
import "./style.css";

function LandingPage() {
  return (
    <>
      <Navbar />
      <div className="spacer"></div>

      <div className="main-section">
        {/* Quote Section */}
        <div className="quote-container">
          <img
            src="https://www.shutterstock.com/image-photo/agriculturist-utilize-core-data-network-600nw-1884814591.jpg"
            alt="Farm background"
            className="quote-bg"
          />
          <div className="quote-overlay">
            <div className="quote-content">
              {/* <img src="/side-image.png" alt="Side visual" className="quote-side-img" /> */}
              <div className="quote-text-block">
                <h1 className="quote-text">"Smart Farming is Caring"</h1>
                <p className="quote-sub">Empowering farmers with technology</p>
              </div>
            </div>
          </div>
        </div>

        {/* What We Do Section */}
        <div className="what-we-do">
          <img src="/image.jpg" alt="What we do" className="what-we-do-img" />
          <div className="what-we-do-text">
            <h2>What We Do</h2>
            <p>
              At PureHarvest, we empower farmers with modern tools and AI-based solutions
              for efficient farming. Our goal is to increase yield, prevent disease, and
              promote sustainable agriculture through smart technology.
            </p>
          </div>
        </div>
      </div>

      <UploadImage />
    </>
  );
}

export default LandingPage;
