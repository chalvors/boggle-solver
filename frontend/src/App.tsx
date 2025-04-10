import { useState } from "react";

export const BASE_URL = "http://localhost:5000/api";

function App() {

  const [loadingBoard, setLoadingBoard] = useState(false);
  const [loadingWords, setLoadingWords] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const [words, setWords] = useState<String[] | null>(null);
  const [board, setBoard] = useState<String[][] | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {

    if (e.target.files) {
      setFile(e.target.files[0]);
    }
  }

  const handleUpload = async () => {

    setBoard(null);
    setWords(null);

    if (file && !loadingBoard && !loadingWords) {

      setLoadingBoard(true);

      const formData = new FormData();
      formData.append('image', file);

      try {
        
        const result = await fetch(BASE_URL + "/detect", {
          method: "PUT",
          body: formData,
        });

        const data = await result.json();
        setBoard(data["board"]);
        setLoadingBoard(false);
        

      } catch (error) {
        console.error(error);
      }
    }
  }

  const handleSolve = async () => {
  
    setLoadingWords(true);

    try {
        
      const result = await fetch(BASE_URL + "/solve", {
        method: "PUT",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(board),
      });

      const data = await result.json();
      setWords(data["words"]);
      setLoadingWords(false);
      

    } catch (error) {
      console.error(error);
    }

  }

  const handleEdit = () => {
    console.log('edit board')
  }

  const renderBoard = () => {
    if (loadingBoard) {
      return (
        <p>Detecting Board</p>
      )
    }

    if (board) {
      return (
        <div>
            <p>Board Found:</p>
            {
              board.map((row) => {
                return (
                  <p key={row.toString()}>{row}</p>
                )
              })
            }

            <button onClick={handleSolve}>Solve Board</button>
            <button onClick={handleEdit}>Edit Board</button>
        </div>   
      )
    }
  }

  const renderWords = () => {
    if (!loadingBoard) {

      if (loadingWords) {
        return (
          <p>Finding Words</p>
        )
      }

      if (words) {
        return (
          <div>
              <p>Words Found:</p>
              <ul>
              {
                words.map((word) => {
                  return (
                    <p key={word.toString()}>{word}</p>
                  )
                })
              }
              </ul>
          </div>   
        )
      }
    }
  }

  return (
    <div style={{marginTop: '40px'}}>
      <input type="file" name="image" onChange={handleFileChange}></input>
      <button onClick={handleUpload}>upload</button>

      {renderBoard()}
      {renderWords()}

    </div>
  )
}

export default App
