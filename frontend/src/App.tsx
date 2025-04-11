import { useState, useCallback } from "react";
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
  const [enteringManually, setEnteringManually] = useState(false);

  const getNumErrors = useCallback(() => {
    
    if (board) {
      let errors = 0;

      for (const row of board) {
        for (const char of row) {
          if (char === '?') {
            errors += 1;
          }
        }
      }
      return errors
    }
    return undefined

  }, [board]);

  const boardHasErrors = (Number(getNumErrors()) > 0);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {

    if (e.target.files) {

      setEnteringManually(false);

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

  const handleClear = () => {
    if (!loadingWords) {
      setFile(null);
      setBoard(null);
      setWords(null);
    }
  }

  function fileIsImage(file: File) {
    return file.type.includes('image');
  }

  const handleManualEnter = () => {

    const newBoard = [
      ['?', '?', '?', '?'],
      ['?', '?', '?', '?'],
      ['?', '?', '?', '?'],
      ['?', '?', '?', '?']
    ]

    setBoard(newBoard);
    setEnteringManually(true);
  }

  const renderBoard = () => {

    if (!loadingBoard && !board) {
      return (
        <div>
          <FileSelectorButton htmlFor="file-upload">
            Take Photo
          </FileSelectorButton>
          <input 
            id='file-upload'
            type='file'
            name='image'
            onChange={handleFileChange} 
            style={{display: 'none'}}
          />

          <BoardButton style={{marginTop: '30px'}} onClick={handleManualEnter}>Manually Enter</BoardButton>
          
          { 
            file &&
              <div>
                <p>{file.name}</p>
                {fileIsImage(file) ? <BoardButton onClick={handleUpload}>Upload</BoardButton> : <p>please select an image file</p>}
              </div>
          }
          
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
                        <Cell key={index} errorCell={char === '?'}>{char}</Cell>
                      )
                    })
                  )
                })
              }
            </GridContainer>

            {boardHasErrors && !enteringManually && <p>could not read {getNumErrors()} cells</p>}
            {getNumErrors() === 16 && !enteringManually ? <p>please take another picture</p> : <p>please edit any missing or incorrect cells</p>}

            <Buttons>
              <BoardButton onClick={handleSolve} disabled={loadingWords || boardHasErrors}>Solve</BoardButton>
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

const Cell = styled.div<{errorCell: boolean}>`
  background-color: ${props => props.errorCell ? '#9966cc' : 'white'};
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

const FileSelectorButton = styled.label`
  border: 2px solid black;
  background-color: white;
  margin: 10px;
  width: 100px;
  height: 33px;
  padding-top: 10px;
  padding-bottom: 10px;
  padding-left: 12px;
  padding-right: 12px;
`;