import { useRef, useState } from "react";

export const BASE_URL = "http://localhost:5000/api";

function App() {

  const [loading, setLoading] = useState(false);
  const [file, setFile] = useState<File | null>(null)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {

    if (e.target.files) {
      setFile(e.target.files[0]);
    }
  }

  const handleUpload = async () => {

    if (file) {

      setLoading(true);
      
      console.log("send image to back end");

      const formData = new FormData();
      formData.append('image', file);

      try {
        
        const result = await fetch(BASE_URL + "/solve", {
          method: "PUT",
          body: formData,
        });

        const data = await result.json();
        setLoading(false);
        console.log(data);
        

      } catch (error) {
        console.error(error);
      }
    }
  }

  return (
    <div style={{marginTop: '40px'}}>
      <input type="file" name="image" onChange={handleFileChange}></input>
      <button onClick={handleUpload}>upload</button>

      <p>Loading: {loading.toString()}</p>
    </div>
  )
}

export default App
