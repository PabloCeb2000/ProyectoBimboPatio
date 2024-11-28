import React, { useState } from "react";
import TopLeftCroquisPopup from "./TopLeftCroquisPopup";
import TopRightCroquisPopup from "./TopRightCroquisPopup";
import BottomLeftCroquisPopup from "./BottomLeftCroquisPopup";
import BottomRightCroquisPopup from "./BottomRightCroquisPopup";

const Croquis = ({ data }) => {
  const [hoveredSection, setHoveredSection] = useState(null);

  return (
    <>
      <div
        className="relative w-full h-full bg-cover bg-center flex rounded-2xl"
        style={{
          backgroundImage: "url('public/croquis.jpeg')",
          borderRadius: "16px",
        }}
      >
        {/* Top Left Section */}
        <div
          className="w-1/2 h-1/2 absolute top-0 left-0"
          onMouseEnter={() => setHoveredSection("topLeft")}
          onMouseLeave={() => setHoveredSection(null)}
        >
          {hoveredSection === "topLeft" && (
            <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-violet-800 bg-opacity-70 text-white p-6 rounded-lg w-3/4 h-3/4 flex items-center justify-center">
              <TopLeftCroquisPopup
                total={data.zona1.total}
                cargado={data.zona1.cargado}
                inactivos={data.zona1.inactivos}
                vacio={data.zona1.vacio}
              />
            </div>
          )}
        </div>

        {/* Top Right Section */}
        <div
          className="w-1/2 h-1/2 absolute top-0 right-0"
          onMouseEnter={() => setHoveredSection("topRight")}
          onMouseLeave={() => setHoveredSection(null)}
        >
          {hoveredSection === "topRight" && (
            <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-orange-800 bg-opacity-70 text-white p-6 rounded-lg w-3/4 h-3/4 flex items-center justify-center">
              <TopRightCroquisPopup
                total={data.zona3.total}
                cargado={data.zona3.cargado}
                inactivos={data.zona3.inactivos}
                vacio={data.zona3.vacio}
              />
            </div>
          )}
        </div>

        {/* Bottom Left Section */}
        <div
          className="w-1/2 h-1/2 absolute bottom-0 left-0"
          onMouseEnter={() => setHoveredSection("bottomLeft")}
          onMouseLeave={() => setHoveredSection(null)}
        >
          {hoveredSection === "bottomLeft" && (
            <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-blue-800 bg-opacity-70 text-white p-6 rounded-lg w-3/4 h-3/4 flex items-center justify-center">
              <BottomLeftCroquisPopup
                total={data.zona2.total}
                cargado={data.zona2.cargado}
                inactivos={data.zona2.inactivos}
                vacio={data.zona2.vacio}
              />
            </div>
          )}
        </div>

        {/* Bottom Right Section */}
        <div
          className="w-1/2 h-1/2 absolute bottom-0 right-0"
          onMouseEnter={() => setHoveredSection("bottomRight")}
          onMouseLeave={() => setHoveredSection(null)}
        >
          {hoveredSection === "bottomRight" && (
            <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-green-800 bg-opacity-70 text-white p-6 rounded-lg w-3/4 h-3/4 flex items-center justify-center">
              <BottomRightCroquisPopup
                total={data.zona4.total}
                cargado={data.zona4.cargado}
                inactivos={data.zona4.inactivos}
                vacio={data.zona4.vacio}
              />
            </div>
          )}
        </div>
      </div>
    </>
  );
};

export default Croquis;
