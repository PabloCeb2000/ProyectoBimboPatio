import React, { useState, useEffect } from 'react';
import nextDeparturesData from './SendOrders.json';

function NextDeparturesTable() {
  const [data, setData] = useState(nextDeparturesData);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedColumn, setSelectedColumn] = useState('');
  const [filteredData, setFilteredData] = useState(nextDeparturesData);
  const [rangeFilter, setRangeFilter] = useState({ min: '', max: '' });
  const [stringFilter, setStringFilter] = useState('');
  const [globalDateFilter, setGlobalDateFilter] = useState({ startDate: '', endDate: '' });
  const [loading, setLoading] = useState(true);

  const columnHeaders = [
    "FECHA DE CIERRE",
    "CARGA",
    "ORDEN",
    "FECHA DE ENVIO",
    "ITEM",
    "DESCRIPCION",
    "CANTIDAD",
    "LPN",
    "ORIGEN",
    "NOMBRE ORIGEN",
    "PLATE NUMBER"
  ];

  // Helper function to check if the selected column contains string values
  const isStringColumn = () => {
    return data.length > 0 && typeof data[0][selectedColumn] === 'string';
  };

  useEffect(() => {

    /*
    const fetchData = async () => {
      try {
        const response = await fetch('https://api.example.com/nextArrivals'); 
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const result = await response.json();
        setData(result);
        setFilteredData(result); 
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
    */
    setLoading(false); // Set loading to false since we are using JSON data
  }, []);

  useEffect(() => {
    let filtered = data;

    // Apply search term filter
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

    // Apply range filter if numeric column and min/max are specified
    if (selectedColumn && !isStringColumn() && rangeFilter.min !== '' && rangeFilter.max !== '') {
      const min = parseFloat(rangeFilter.min);
      const max = parseFloat(rangeFilter.max);
      filtered = filtered.filter((row) => {
        const value = parseFloat(row[selectedColumn]);
        return value >= min && value <= max;
      });
    }

    // Apply string filter if selected column is a string
    if (selectedColumn && isStringColumn() && stringFilter) {
      filtered = filtered.filter((row) => 
        row[selectedColumn]?.toLowerCase().includes(stringFilter.toLowerCase())
      );
    }

    // Apply global date range filter if startDate and endDate are specified
    if (globalDateFilter.startDate && globalDateFilter.endDate) {
      const startDate = new Date(globalDateFilter.startDate);
      const endDate = new Date(globalDateFilter.endDate);

      filtered = filtered.filter((row) =>
        Object.values(row).some((value) => {
          const dateValue = new Date(value);
          return !isNaN(dateValue) && dateValue >= startDate && dateValue <= endDate;
        })
      );
    }

    setFilteredData(filtered);
  }, [searchTerm, selectedColumn, rangeFilter, stringFilter, globalDateFilter, data]);

  // Update range or string filter
  const handleRangeChange = (e) => {
    setRangeFilter({ ...rangeFilter, [e.target.name]: e.target.value });
  };

  const handleStringFilterChange = (e) => {
    setStringFilter(e.target.value);
  };

  // Update global date filter
  const handleGlobalDateChange = (e) => {
    setGlobalDateFilter({ ...globalDateFilter, [e.target.name]: e.target.value });
  };

  const handleResetFilters = () => {
    setSearchTerm('');
    setSelectedColumn('');
    setRangeFilter({ min: '', max: '' });
    setStringFilter('');
    setGlobalDateFilter({ startDate: '', endDate: '' });
  };

  if (loading) return <p>Loading...</p>;

  return (
    <div className="next-departures-table-container">
      {/* Global Date Filter */}
      <div className="flex gap-4 mb-4">
        <input
          type="date"
          name="startDate"
          placeholder="Start Date"
          value={globalDateFilter.startDate}
          onChange={handleGlobalDateChange}
          className="text-black p-2 border rounded"
        />
        <input
          type="date"
          name="endDate"
          placeholder="End Date"
          value={globalDateFilter.endDate}
          onChange={handleGlobalDateChange}
          className="text-black p-2 border rounded"
        />
      </div>

      {/* Search and Column Selector */}
      <div className="flex gap-4 mb-4">
        <input
          type="text"
          placeholder="Search..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="text-black p-2 border rounded"
        />

        {/* Column Selector */}
        <select
          value={selectedColumn}
          onChange={(e) => {
            setSelectedColumn(e.target.value);
            setRangeFilter({ min: '', max: '' }); // Reset filters when column changes
            setStringFilter('');
          }}
          className="p-2 border rounded text-black"
        >
          <option value="">All Columns</option>
          {columnHeaders.map((col) => (
            <option key={col} value={col}>
              {col}
            </option>
          ))}
        </select>

        <button 
          className='bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded'
          onClick={() => {handleResetFilters()}}
        >
          Borrar Filtros 
        </button>
      </div>

      {/* Range or String Filter */}
      {selectedColumn && (
        <div className="flex gap-4 mb-4">
          {isStringColumn() ? (
            <input
              type="text"
              placeholder="Enter value"
              value={stringFilter}
              onChange={handleStringFilterChange}
              className="text-black p-2 border rounded"
            />
          ) : (
            <>
              <input
                type="number"
                name="min"
                placeholder="Min"
                value={rangeFilter.min}
                onChange={handleRangeChange}
                className="text-black p-2 border rounded"
              />
              <input
                type="number"
                name="max"
                placeholder="Max"
                value={rangeFilter.max}
                onChange={handleRangeChange}
                className="text-black p-2 border rounded"
              />
            </>
          )}
        </div>
      )}

      {/* Table */}
      <div className="overflow-auto" style={{ maxHeight: '400px', maxWidth: '100%' }}>
        <table className="min-w-full border-collapse">
          <thead className="bg-[#293038] text-white sticky top-0">
            <tr>
              {columnHeaders.map((col) => (
                <th key={col} className="px-4 py-2 border border-gray-400">{col}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {filteredData.map((row, index) => (
              <tr key={index} className="hover:bg-slate-600">
                {columnHeaders.map((col, i) => (
                  <td key={i} className="px-4 py-2 border border-gray-400">
                    {row[col] || ''}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default NextDeparturesTable;
