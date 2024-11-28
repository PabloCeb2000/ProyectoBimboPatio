import React, { useState } from "react";
import Loader from "./Loader";
import axios from "axios";

const PrioridadDescarga = () => {
  const [dataForm, setDataForm] = useState({
    num_fosas: 0,
    status: "Todas",
    peso_fecha: 0,
    peso_ganancia: 0,
    peso_cantidad: 0,
  });
  const [error, setError] = useState(false);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [showTable, setShowTable] = useState(false);
  const [tableData, setTableData] = useState({});

  const checkEmptyFields = () => {
    for (const key in dataForm) {
      if (dataForm[key] === "" || dataForm[key] === 0) {
        return true;
      }
    }
    return false;
  };

  const handlePostData = async (e) => {
    e.preventDefault();

    if (checkEmptyFields()) {
      setMessage("Please fill in all fields correctly.");
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post(
        "http://localhost:8000/bimboC/priorize_trucks/",
        JSON.stringify(dataForm), // Convierte el objeto a JSON explícitamente
        {
          headers: {
            "Content-Type": "application/json", // Asegura el tipo de contenido
          },
        }
      );
      if (response.status === 200) {
        setTableData(response.data.embarks || {});
        setShowTable(true);
        setMessage("");
      }
    } catch (error) {
      console.error("Error fetching data:", error);
      setError(true);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <Loader />;

  return (
    <div className="max-w-3xl mx-auto bg-[#1c1d21] text-white shadow-md rounded-lg p-6">
      {error && (
        <p className="text-red-500 text-center font-semibold mt-4">
          Error sending or fetching data.
        </p>
      )}
      {showTable ? (
        <div>
          <h2 className="text-xl font-bold mb-4">Embark Details</h2>
          <table className="w-full text-left table-auto bg-[#293038] rounded-md">
            <thead>
              <tr className="text-gray-400 border-b border-gray-600">
                <th className="px-4 py-2">Num Embark</th>
                <th className="px-4 py-2">Status</th>
                <th className="px-4 py-2">Truck Number</th>
                <th className="px-4 py-2">Truck Location</th>
              </tr>
            </thead>
            <tbody>
              {Object.keys(tableData).map((key) => {
                const embark = tableData[key];
                return (
                  <tr
                    key={embark.num_embark}
                    className="border-b border-gray-600"
                  >
                    <td className="px-4 py-2">{embark.num_embark}</td>
                    <td className="px-4 py-2">{embark.status}</td>
                    <td className="px-4 py-2">{embark.truck_number}</td>
                    <td className="px-4 py-2">{embark.truck_location}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
          <button
            onClick={() => setShowTable(false)}
            className="mt-4 bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600 transition-colors"
          >
            Recalculate Priority
          </button>
        </div>
      ) : (
        <div>
          <h2 className="text-xl font-bold mb-6">Unload Priority Form</h2>
          <form onSubmit={handlePostData} className="space-y-4">
            <div>
              <label className="font-semibold block">Number of Pits</label>
              <input
                type="number"
                placeholder="Number of pits"
                required
                value={dataForm.num_fosas}
                onChange={(e) =>
                  setDataForm({
                    ...dataForm,
                    num_fosas: parseInt(e.target.value),
                  })
                }
                className="bg-[#293038] w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="font-semibold block">Status</label>
              <select
                required
                value={dataForm.status}
                onChange={(e) =>
                  setDataForm({ ...dataForm, status: e.target.value })
                }
                className="bg-[#293038] w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="Todas">Todas</option>
                <option value="Disponible en patio">Disponible en patio</option>
                <option value="En ruta">En ruta</option>
              </select>
            </div>
            <div>
              <label className="font-semibold block">Date</label>
              <input
                type="number"
                placeholder="Date"
                required
                value={dataForm.peso_fecha}
                onChange={(e) =>
                  setDataForm({
                    ...dataForm,
                    peso_fecha: parseFloat(e.target.value),
                  })
                }
                className="bg-[#293038] w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="font-semibold block">Earnings</label>
              <input
                type="number"
                placeholder="Earnings"
                required
                value={dataForm.peso_ganancia}
                onChange={(e) =>
                  setDataForm({
                    ...dataForm,
                    peso_ganancia: parseFloat(e.target.value),
                  })
                }
                className="bg-[#293038] w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="font-semibold block">Amount</label>
              <input
                type="number"
                placeholder="Amount"
                required
                value={dataForm.peso_cantidad}
                onChange={(e) =>
                  setDataForm({
                    ...dataForm,
                    peso_cantidad: parseFloat(e.target.value),
                  })
                }
                className="bg-[#293038] w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            {message && (
              <p className="text-red-500 text-center font-semibold">
                {message}
              </p>
            )}
            <button
              type="submit"
              className="w-full bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600 transition-colors"
            >
              Send Data
            </button>
          </form>
        </div>
      )}
    </div>
  );
};

export default PrioridadDescarga;
