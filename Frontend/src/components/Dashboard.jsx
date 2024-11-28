import React, { useEffect, useState } from "react";
import Croquis from "./Croquis";
import NextArrivals from "./NextArrivals";
import Orders from "./Orders";
import NextDepartures from "./SendOrders";
import box from "/box.svg";
import truck from "/truck.svg";
import truckFast from "/truck-fast.svg";
import LiveTrucks from "./LiveTrucks";
import PrioridadDescarga from "./PrioridadDescarga";

function Dashboard() {
  const [selectedComponent, setSelectedComponent] = useState("Croquis");
  const [TruckSocket, setTruckSocket] = useState(null);
  // Esto se inicializará vacío, ahora para ejemplificar
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Se va a inicializar vacío, pero se va a llenar con los datos que se reciban del WebSocket
  const[zonasTotal, setZonasTotal] = useState({
    zona1: {
      total: 0,
      cargado: 0,
      inactivos: 0,
      vacio: 0,
    },
    zona2: {
      total: 0,
      cargado: 0,
      inactivos: 0,
      vacio: 0,
    },
    zona3: {
      total: 0,
      cargado: 0,
      inactivos: 0,
      vacio: 0,
    },
    zona4: {
      total: 0,
      cargado: 0,
      inactivos: 0,
      vacio: 0,
    },
  });

  const columnHeaders = [
    "Truck Number",
    "Location",
    "Status",
    "Size",
  ]

  useEffect(() => {
    const fetchLiveTruckData = async () => {
      setLoading(true);
      try {
        const response = await fetch("http://127.0.0.1:8000/bimboC/trucks/");
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        const result = await response.json();
  
        const flattenedData = result.map((truck) => ({
          Truck_Number: truck?.truck_number || "",
          Location: truck?.location || "",
          Status: truck?.status || "",
          Size: truck?.size || "",
        }));
  
        setData(flattenedData);
  
        const calculateZonaData = (zonaName) => {
          const total = flattenedData.filter((truck) => truck.Location === zonaName).length;
          const cargado = flattenedData.filter(
            (truck) => truck.Location === zonaName && truck.Status === "En patio"
          ).length;
          const inactivos = flattenedData.filter(
            (truck) => truck.Location === zonaName && truck.Status === "No disponible"
          ).length;
          const vacio = flattenedData.filter(
            (truck) => truck.Location === zonaName && truck.Status === "Vacio"
          ).length;
  
          return { total, cargado, inactivos, vacio };
        };
  
        setZonasTotal({
          zona1: calculateZonaData("Zona 1"),
          zona2: calculateZonaData("Zona 2"),
          zona3: calculateZonaData("Zona 3"),
          zona4: calculateZonaData("Zona 4"),
        });
      } catch (error) {
        console.error(error);
        setError(true);
      } finally {
        setLoading(false);
      }
    };
  
    fetchLiveTruckData();
    const fetchInterval = setInterval(fetchLiveTruckData, 10000);
    return () => clearInterval(fetchInterval);
  }, []);  

  const renderComponent = () => {
    switch (selectedComponent) {
      case "Croquis":
        return <Croquis data={zonasTotal} />;
      /* case "Inventory":
        return <Inventory />; */
      case "nextArrivals":
        return <NextArrivals />;
      case "orders":
        return <Orders />;
      case "prioridadDescargas":
        return <PrioridadDescarga />;
      case "nextDepartures":
        return <NextDepartures />;
      default:
        return <Croquis data={zonasTotal} />;
    }
  };

  // Check if selected component is either "nextArrivals" or "orders"
  const isShrunk =
    selectedComponent === "nextArrivals" || selectedComponent === "orders";

  return (
    <div className="flex flex-col h-screen">
      {/* Navbar */}
      <div className="flex items-center justify-between bg-[#1c1d21] text-white px-6 py-4 border-b-2 border-slate-300">
        <div className="text-4xl font-thin">Bimbo Dashboard</div>
        <div className="relative">{/* SVG Icon */}</div>
      </div>

      <div className="flex flex-row h-full">
        {/* Sidebar */}
        <div className="w-2/12 bg-[#1c1d21] text-white flex flex-col gap-4 p-6">
          <h1 className="text-2xl font-normal mb-2">Seguimientos en vivo</h1>
          <div
            onClick={() => setSelectedComponent("Graphics")}
            className="flex items-center gap-3 px-3 py-2 rounded-xl bg-[#293038] hover:bg-slate-600 cursor-pointer"
          >
            <p className="text-white text-sm font-medium leading-normal">
              General
            </p>
          </div>
          <div
            onClick={() => setSelectedComponent("nextArrivals")}
            className="flex items-center gap-3 px-3 py-2 rounded-xl bg-[#293038] hover:bg-slate-600 cursor-pointer"
          >
            <img src={truck} alt="Next Arrivals" className="h-6 w-6" />
            <p className="text-white text-sm font-medium leading-normal">
              Próximas llegadas
            </p>
          </div>
          <div
            onClick={() => setSelectedComponent("orders")}
            className="flex items-center gap-3 px-3 py-2 rounded-xl bg-[#293038] hover:bg-slate-600 cursor-pointer"
          >
            <img src={box} alt="Orders" className="h-6 w-6" />
            <p className="text-white text-sm font-medium leading-normal">
              Ordenes
            </p>
          </div>
          <div
            onClick={() => setSelectedComponent("prioridadDescargas")}
            className="flex items-center gap-3 px-3 py-2 rounded-xl bg-[#293038] hover:bg-slate-600 cursor-pointer"
          >
            <img src={truckFast} alt="Orders" className="h-6 w-6" />
            <p className="text-white text-sm font-medium leading-normal">
              Prioridad Descargas
            </p>
          </div>
          {/* <div
            onClick={() => setSelectedComponent("nextDepartures")}
            className="flex items-center gap-3 px-3 py-2 rounded-xl bg-[#293038] hover:bg-slate-600 cursor-pointer"
          >
            <img src={truckFast} alt="Send Orders" className="h-6 w-6" />
            <p className="text-white text-sm font-medium leading-normal">Próximas Salidas</p>
          </div> */}
        </div>

        {/* Main Content Area */}
        <div className={`flex flex-col ${isShrunk ? "w-6/12" : "w-5/12"}`}>
          <div className="flex-1 p-8 bg-[#1c1d21]">{renderComponent()}</div>
        </div>

        {/* Right Sidebar */}
        {error ? (
          <p className="text-white">Error fetching truck data</p>
        ) : (
          <div
            className={`flex flex-col gap-4 p-6 text-white bg-[#1c1d21] ${
              isShrunk ? "w-4/12" : "w-5/12"
            }`}
          >
            <h1 className="text-2xl font-normal mb-2">Camiones en Patio</h1>
            <LiveTrucks data={data} />
          </div>
        )}
      </div>
    </div>
  );
}

export default Dashboard;
