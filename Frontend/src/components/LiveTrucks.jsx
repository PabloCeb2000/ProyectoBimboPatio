import React from "react";

const LiveTrucks = ({ data }) => {
  return (
    <>
      {data.length === 0 ? (
        <p className="text-white text-center">No hay camiones disponibles</p>
      ) : (
        <table className="min-w-full bg-[#293038] text-white rounded-xl">
          <thead>
            <tr>
              <th className="py-2 px-4 border-b border-gray-700">ID</th>
              <th className="py-2 px-4 border-b border-gray-700">Zone</th>
              <th className="py-2 px-4 border-b border-gray-700">Status</th>
              <th className="py-2 px-4 border-b border-gray-700">Size</th>
              {/* <th className="py-2 px-4 border-b border-gray-700">Hora de llegada</th> */}
            </tr>
          </thead>
          <tbody>
            {data.map((item, index) => (
              <tr key={index} className="hover:bg-slate-600">
                <td className="py-2 px-4 border-b border-gray-700 text-center">
                  {item.Truck_Number}
                </td>
                <td className="py-2 px-4 border-b border-gray-700 text-center">
                  {item.Location}
                </td>
                <td
                  className={`py-2 px-4 border-b border-gray-700 text-center ${
                    item.Status === "Cargado"
                      ? "text-green-400"
                      : item.Status === "No Disponible"
                      ? "text-red-400"
                      : "text-orange-300"
                  }`}
                >
                  {item.Status}
                </td>
                <td className="py-2 px-4 border-b border-gray-700 text-center">
                  {item.Size}
                </td>
                {/* <td className="py-2 px-4 border-b border-gray-700 text-center">{item.horaDeLlegada}</td> */}
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </>
  );
};

export default LiveTrucks;
