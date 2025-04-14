import { useState, useCallback, BaseSyntheticEvent, useRef } from 'react';
import styled from 'styled-components';
import { Spinner } from 'react-spinner-toolkit';
import Modal from '@mui/material/Modal';
import Box from '@mui/material/Box';

export const BASE_URL = "http://localhost:5000/api";
export const BOARD_SIZE = 4;

export interface ModalProps {
  value: string,
  cellPos: CellPos
}

export interface CellPos {
  xCord: number,
  yCord: number
}

function App() {

  const [loadingBoard, setLoadingBoard] = useState(false);
  const [loadingWords, setLoadingWords] = useState(false);
  const [words, setWords] = useState<String[] | null>(null);
  const [board, setBoard] = useState<String[][] | null>(null);
  const [enteringManually, setEnteringManually] = useState(false);
  const [editedCells, setEditedCells] = useState<CellPos[]>([]);

  const [openModal, setOpenModal] = useState(false);
  const [modalInfo, setModalInfo] = useState<ModalProps>({value: '', cellPos: {xCord: -1, yCord: -1}});
  const modalInputRef = useRef<HTMLInputElement>(null);

  function fileIsImage(file: File) {
    return file.type.includes('image');
  }

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

  const boardHasErrors = useCallback(() => {

    return Number(getNumErrors()) > 0;

  }, [getNumErrors]);

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {

    if (e.target.files) {

      const newFile = e.target.files[0];

      setEnteringManually(false);

      if (fileIsImage(newFile)) {

        setBoard(null);
        setWords(null);

        setLoadingBoard(true);

        const formData = new FormData();
        formData.append('image', newFile);

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
      else {
        console.error('ERROR file is not an image: "' + newFile.name + '" is of type "' + newFile.type + '"');
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
      setEditedCells([]);
      setBoard(null);
      setWords(null);
    }
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

  const handleCloseModal = () => {

    const newValue = modalInputRef.current?.value;

    if (newValue?.match('[A-Z]')) {

      let newBoard = board;

      if (newBoard && newValue) {

        newBoard[modalInfo.cellPos.xCord][modalInfo.cellPos.yCord] = newValue.toUpperCase();

        setBoard(newBoard);

        const cellPos: CellPos = {
          xCord: modalInfo.cellPos.xCord,
          yCord:  modalInfo.cellPos.yCord
        }
        let newEditedCells = editedCells;

        if (!newEditedCells.some(cell => cell.xCord === cellPos.xCord && cell.yCord === cellPos.yCord)) {
          newEditedCells.push(cellPos);
          setEditedCells(newEditedCells);
        }

        setOpenModal(false);
      }
    }
  }

  const handleCellClick = (e: BaseSyntheticEvent, i: number, j: number) => {

    const value = e.target.innerHTML;

    const props: ModalProps = {
      value: value,
      cellPos: {
        xCord: i,
        yCord: j
      }
    }

    setModalInfo(props);
    setOpenModal(true);
  }

  const handleModalInputKeyDown = (e: any) => {
    if (e.code === 'Enter') {
      handleCloseModal();
    }
  }

  const renderNumErrorCells = () => {
    if (boardHasErrors() && !enteringManually) {
      return (
        <p>could not read {getNumErrors()} cells</p>
      )
    }
  }

  const renderTakeAnotherPicture = () => {
    if (Number(getNumErrors()) === 16 && !enteringManually) {
      return (
        <>
          <p>please take another picture</p>
          <p>make sure the image is clear and the board is centered</p>
        </>
      )
    }
  }

  const renderPleaseEdit = () => {
    if (Number(getNumErrors()) > 0 && Number(getNumErrors()) < 16 ||
        Number(getNumErrors()) > 0 && enteringManually
    ) {
      return (
        <p>please edit any missing or incorrect cells</p>
      )
    }
  }

  const handleModalInputFocus = (e: BaseSyntheticEvent) => {
    e.target.select();
  }

  const renderBoard = () => {

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
                board.map((row, i) => {
                  return (
                    row.map((char, j) => {

                      const cellHasBeenEdited = editedCells.some(cell => cell.xCord === i && cell.yCord === j);

                      return (
                        <Cell key={j} $error={char === '?'} $edited={cellHasBeenEdited} onClick={(e)=>{handleCellClick(e, i, j)}}>{char}</Cell>
                      )
                    })
                  )
                })
              }
            </GridContainer>

            {renderNumErrorCells()}
            {renderTakeAnotherPicture()}
            {renderPleaseEdit()}

            <Buttons>
              <BoardButton onClick={handleSolve} disabled={loadingWords || boardHasErrors()}>Solve</BoardButton>
              <BoardButton onClick={handleClear} disabled={loadingWords}>Clear</BoardButton>
            </Buttons>

            <Modal
              open={openModal}
              onClose={handleCloseModal}
            >
              <Box sx={modalStyle}>
                <ModalDiv>
                  <h1>{`Edit Cell (${modalInfo.cellPos.xCord},${modalInfo.cellPos.yCord})`}</h1>
                  <input
                    defaultValue={modalInfo.value}
                    autoFocus={true}
                    onFocus={handleModalInputFocus}
                    onKeyDown={(e)=>{handleModalInputKeyDown(e)}}
                    ref={modalInputRef}
                  />
                  <BoardButton onClick={handleCloseModal}>OK</BoardButton>
                </ModalDiv>
              </Box>
            </Modal>

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

  const handleTakePhotoClick = () => {
    const input = document.getElementById('file-upload');

    if(input) {
      input.click();
    }
  }

  const renderInitialButtons = () => {
    if (!loadingBoard && !board) {
      return (
        <InitialButtonsDiv>
          <div>
            <InitialButton onClick={handleTakePhotoClick}>Take Photo</InitialButton>
          </div>

          <div>
            <input 
              id='file-upload'
              type='file'
              name='image'
              onChange={handleFileChange} 
              style={{display: 'none'}}
            />
          </div>

          <div>
            <InitialButton style={{marginTop: '30px'}} onClick={handleManualEnter}>Enter Manually</InitialButton>
          </div>
          
        </InitialButtonsDiv>
      )
    }
  }

  return (
    <AppContainer>
      {renderInitialButtons()}
      {renderBoard()}
      {renderWords()}
    </AppContainer>
  )
}

export default App

const AppContainer = styled.div`
  width: 100%;
  height: 100%;
  text-align: center;
`;

const InitialButtonsDiv = styled.div`
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  padding-bottom: 60px;
`;

const GridContainer = styled.div`
  display: grid;
  grid-template-columns: repeat(${BOARD_SIZE}, auto);
  background-color: black;
  padding: 10px;
  margin: 20px;
`;

const Cell = styled.div<{ $error?: boolean; $edited?: boolean}>`
  background-color: ${props => props.$edited ? '#88da68' : props.$error ? '#da6868' : '#62ccec'};
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
  text-align: center;
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

const modalStyle = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 200,
  bgcolor: 'background.paper',
  border: '2px solid #000',
  boxShadow: 24,
  p: 4,
};

const ModalDiv = styled.div`
  text-align: center;
`;

const InitialButton = styled.button`
  width: 80%;
  height: 60px;
  margin: 12px;
  border-radius: 12px;
  background-color: #42b6e4;
  color: black;
  font-family: Lexend;
  font-size: 16px;
  text-decoration: none;
  text-align: center;
  &:active{
    transform: translateY(4px);
  }
`;


//TODO
// guard for editing cells
//  - force caps in input?
//    - intercept on change and change input to caps
//  - only 1 letter or 'QU'
//  - keep cells the same size no matter the contents