import React, { useState, useEffect } from "react";
import Loader from "./Loader";

function NextArrivalsTable() {
  const [data, setData] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedColumn, setSelectedColumn] = useState("");
  const [filteredData, setFilteredData] = useState([]);
  const [rangeFilter, setRangeFilter] = useState({ min: "", max: "" });
  const [globalDateFilter, setGlobalDateFilter] = useState({
    startDate: "",
    endDate: "",
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const rowsPerPage = 20; // Rows per page

  const columnHeaders = [
    "ID",
    "Close Date",
    "LPN",
    "Order",
    "Product ID",
    "Product Description",
    "Quantity",
    "Send Date",
    "Status",
  ];

  useEffect(() => {
    setLoading(true);
    const fetchData = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/bimboC/pendings/");
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        const result = await response.json();

        const flattenedData = result.map((order) => ({
          ID: order?.id || "",
          "Close Date": order?.close_dt || "",
          LPN: order?.lpn || "",
          Order: order?.order || "",
          "Product ID": order?.product?.product || "",
          "Product Description": order?.product?.description || "",
          Quantity: order?.quantity || "",
          "Send Date": order?.send_dt || "",
          Status: order?.status || "",
        }));

        setData(flattenedData);
        setFilteredData(flattenedData);
      } catch (error) {
        console.error("Error fetching data:", error);
        setError(true);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  useEffect(() => {
    let filtered = data;

    if (searchTerm) {
      filtered = filtered.filter((row) => {
        if (selectedColumn) {
          return row[selectedColumn]
            ?.toString()
            .toLowerCase()
            .includes(searchTerm.toLowerCase());
        }
        return Object.values(row).some((value) =>
          value.toString().toLowerCase().includes(searchTerm.toLowerCase())
        );
      });
    }

    if (selectedColumn && rangeFilter.min !== "" && rangeFilter.max !== "") {
      const min = parseFloat(rangeFilter.min);
      const max = parseFloat(rangeFilter.max);
      filtered = filtered.filter((row) => {
        const value = parseFloat(row[selectedColumn]);
        return value >= min && value <= max;
      });
    }

    if (globalDateFilter.startDate && globalDateFilter.endDate) {
      const startDate = new Date(globalDateFilter.startDate);
      const endDate = new Date(globalDateFilter.endDate);
      filtered = filtered.filter((row) => {
        const dateValue = new Date(row["Close Date"]);
        return (
          !isNaN(dateValue) && dateValue >= startDate && dateValue <= endDate
        );
      });
    }

    setFilteredData(filtered);
    setCurrentPage(1); // Reset to the first page when filters change
  }, [searchTerm, selectedColumn, rangeFilter, globalDateFilter, data]);

  const totalPages = Math.ceil(filteredData.length / rowsPerPage);
  const currentData = filteredData.slice(
    (currentPage - 1) * rowsPerPage,
    currentPage * rowsPerPage
  );

  if (loading) return <Loader />;

  return (
    <>
      {error ? (
        <p>Error fetching data</p>
      ) : (
        <div className="next-arrivals-table-container">
          <div className="flex gap-4 mb-4">
            <input
              type="text"
              placeholder="Search..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="text-black p-2 border rounded"
            />
            <select
              value={selectedColumn}
              onChange={(e) => setSelectedColumn(e.target.value)}
              className="p-2 border rounded text-black"
            >
              <option value="">All Columns</option>
              {columnHeaders.map((col) => (
                <option key={col} value={col}>
                  {col}
                </option>
              ))}
            </select>
          </div>

          <div className="overflow-auto" style={{ maxHeight: "400px" }}>
            <table className="min-w-full border-collapse">
              <thead className="bg-gray-800 text-white">
                <tr>
                  {columnHeaders.map((col) => (
                    <th key={col} className="px-4 py-2 border border-gray-400">
                      {col}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {currentData.map((row, index) => (
                  <tr key={index} className="hover:bg-gray-200">
                    {columnHeaders.map((col) => (
                      <td
                        key={col}
                        className="px-4 py-2 border border-gray-400"
                      >
                        {row[col] || ""}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="pagination-controls mt-4">
            <button
              onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))}
              disabled={currentPage === 1}
              className="px-4 py-2 bg-gray-300 rounded disabled:opacity-50"
            >
              Previous
            </button>
            <span className="mx-2">
              Page {currentPage} of {totalPages}
            </span>
            <button
              onClick={() =>
                setCurrentPage((prev) => Math.min(prev + 1, totalPages))
              }
              disabled={currentPage === totalPages}
              className="px-4 py-2 bg-gray-300 rounded disabled:opacity-50"
            >
              Next
            </button>
          </div>
        </div>
      )}
    </>
  );
}

export default NextArrivalsTable;
