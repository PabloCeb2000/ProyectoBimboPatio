import React from 'react'

const BottomRightCroquisPopup = ({total = 0, cargado = 0, inactivos = 0, vacio = 0}) => {
  return (
    <div className='flex flex-col gap-2'>
      <h3 className="text-xl font-medium ">Zona 4: Descarga</h3>
      <h3 className="text-xl font-medium ">Total: {total}</h3>
      <div className="flex flex-col gap-2">
        <div className="flex items-center gap-2">
          <img src="/box.svg" alt="Box" className="h-10 w-10" />
          <p className="text-white text-lg font-medium leading-normal">En patio: <span className="font-bold">{cargado}</span></p>
        </div>
        <div className="flex items-center gap-2">
          <img src="/truck.svg" alt="Truck" className="h-10 w-10" />
          <p className="text-white text-lg font-medium leading-normal">No disponible: <span className="text-red-500 font-bold">{inactivos}</span></p>
        </div>
        <div className="flex items-center gap-2">
          <img src="/truck-fast.svg" alt="Truck" className="h-10 w-10" />
          <p className="text-white text-lg font-medium leading-normal">Vacio: <span className="text-yellow-300 font-bold">{vacio}</span></p>
        </div>
      </div>
    </div>
  )
}

export default BottomRightCroquisPopup