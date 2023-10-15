import { useEffect, useState } from 'react'

function ListWines() {

  const [wines, setWines] = useState([])

  useEffect( () => {
    async function getWines() {
      const base_url = import.meta.env.VITE_BASE_URL
      const res = await fetch(`http://${base_url}/api/`)
      const body = await res.json()
      setWines(body.result)
    }
    getWines()
  }, [])

  const createWineList = () => {
    return wines.map( w => {
      console.log(w)
      console.log(w.wine_name, w.img_url)
      return (
        <>
          <h2 key={w.wine_name}>{w.wine_name}</h2>
          <img src={w.img_url}></img>
        </>
      )
  })
  }


  return(
    <>
      <h2>List Wines</h2>
      {wines && createWineList()}
    </>
  )
}

export default ListWines