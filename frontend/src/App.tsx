import { useState } from "react";
import styled from "styled-components";
import { Spinner } from "react-spinner-toolkit";

export const BASE_URL = "http://localhost:5000/api";
export const BOARD_SIZE = 4;

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

  const handleClear = () => {
    if (!loadingWords) {
      setBoard(null);
      setWords(null);
    }
  }

  const renderBoard = () => {

    if (!loadingBoard && !board) {
      return (
        <div>
          <input 
            type="file" 
            name="image" 
            onChange={handleFileChange} 
          />
          <button onClick={handleUpload}>upload</button>
        </div>
      )
    }

    if (loadingBoard && !board) {
      return (
        <LoadingDiv>
          <LoadingHeader>Detecting Board</LoadingHeader>
          <Spinner 
            size={60}
            color="#007aff"
            loading={loadingBoard}
            animationType="spin"
            shape="circle"
          />
        </LoadingDiv>
      )
    }

    if (board) {
      return (
        <div>
            <GridContainer>
              {
                board.map((row) => {
                  return (
                    row.map((char, index) => {
                      return (
                        <Cell key={index}>{char}</Cell>
                      )
                    })
                  )
                })
              }
            </GridContainer>

            <Buttons>
              <BoardButton onClick={handleSolve} disabled={loadingWords}>Solve</BoardButton>
              <BoardButton onClick={handleEdit} disabled={loadingWords}>Edit</BoardButton>
              <BoardButton onClick={handleClear} disabled={loadingWords}>Clear</BoardButton>
            </Buttons>
        </div>   
      )
    }
  }

  const renderWords = () => {
    if (!loadingBoard) {

      if (loadingWords) {
        return (
          <LoadingDiv>
            <LoadingHeader>Finding Words</LoadingHeader>
            <Spinner 
              size={60}
              color="#007aff"
              loading={loadingWords}
              animationType="spin"
              shape="circle"
            />
          </LoadingDiv>
        )
      }

      if (words) {
        return (
          <WordListContainer>
            {
              words.map((word) => {
                return (
                  <Word key={word.toString()}>{word}</Word>
                )
              })
            }
          </WordListContainer>
        )
      }
    }
  }

  return (
    <AppContainer>
      {renderBoard()}
      {renderWords()}
    </AppContainer>
  )
}

export default App

const AppContainer = styled.div`
  margin-top: 40px;
  text-align: center;
`;

const GridContainer = styled.div`
  display: grid;
  grid-template-columns: repeat(${BOARD_SIZE}, auto);
  background-color: black;
  padding: 10px;
  margin: 20px;
`;

const Cell = styled.div`
  background-color: white;
  border: 1px solid black;
  padding: 10px;
  font-size: 30px;
  text-align: center;
`;

const Buttons = styled.div`
  margin: 20px;
  text-align: center;
`;

const BoardButton = styled.button`
  background-color: white;
  margin: 10px;
  width: 100px;
  height: 33px;
  &:active{
    background-color: lightgray;
    outline: none;
    box-shadow: none;
  }
`;

const WordListContainer = styled.div`
  height: 45vh;
  overflow-y: auto;
`;

const Word = styled.p`
  font-size: 24px;
`;

const LoadingDiv = styled.div`
  justify-items: center;
`;

const LoadingHeader = styled.p`
  margin-bottom: 30px;
`;