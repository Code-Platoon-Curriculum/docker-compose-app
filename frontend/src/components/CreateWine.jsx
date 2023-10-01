import { useState } from 'react'
import { useNavigate } from "react-router-dom"


function CreateWine() {

  const navigate = useNavigate()

  const [wineName, setWineName] = useState()
  const [price, setWinePrice] = useState()
  const [varietal, setWineVarietal] = useState()
  const [description, setWineDescription] = useState()
  const [picture, setWinePicture] = useState()
  const [errors, setErrors] = useState()

  const handleWineNameChange = (e) => setWineName(e.target.value)
  const handleWinePriceChange = (e) => setWinePrice(e.target.value)
  const handleWineVarietalChange = (e) => setWineVarietal(e.target.value)
  const handleWineDescriptionChange = (e) => setWineDescription(e.target.value)
  const handleWineImageChange = (e) => setWinePicture(e.target.files[0])


  const handleSubmit = (e) => {
    e.preventDefault()
    const wineObject = {
      wine_name: wineName,
      price: price,
      varietal: varietal,
      description: description,
      picture: picture
    }
    addWine(wineObject)
  }

  const addWine = async (wineObj) => {
    const base_url = import.meta.env.VITE_BASE_URL
    const url = `http://${base_url}/api/`
    let formData = new FormData()
    formData.append("wine_name", wineObj.wine_name)
    formData.append("price", wineObj.price)
    formData.append("varietal", wineObj.varietal)
    formData.append("description", wineObj.description)
    formData.append("picture", wineObj.picture, wineObj.picture.name)
    const context = {
      method: "POST",
      body: formData
    }
    const resp = await fetch(url, context)
    const body = await resp.json()
    if (resp.status === 400) {
      setErrors(body)
    } else {
      navigate("/")
    }
  }

  return(
    <>
      <h2>Create Wine</h2>
      {errors && <h4>{JSON.stringify(errors)}</h4>}
      <label htmlFor="wineName">Wine Name:</label>
      <input value={wineName} name="wineName" onChange={handleWineNameChange}></input>
      <label htmlFor="winePrice">Wine Price:</label>
      <input value={price} name="winePrice" onChange={handleWinePriceChange}></input>
      <label htmlFor="wineVarietal">Wine Varietal:</label>
      <input value={varietal} name="wineVarietal" onChange={handleWineVarietalChange}></input>
      <label htmlFor="wineDescription">Wine Description:</label>
      <input value={description} name="wineDescription" onChange={handleWineDescriptionChange}></input>
      <label htmlFor="wineImage">Wine Image:</label>
      <input type="file" name="wineImage" onChange={handleWineImageChange}></input>
      <button onClick={handleSubmit}>Submit</button>
    </>
  )}

  export default CreateWine
