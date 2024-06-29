import 'bootstrap/dist/css/bootstrap.min.css'
import {
  useEffect,
  useState,
} from 'react'
import {
  Col,
  Container,
  Navbar,
  Row,
} from 'react-bootstrap'

import AlertDismissible from './components/AlertDismissible.jsx'
import Gallery from './components/Gallery.jsx'
import UploadForm from './components/UploadForm.jsx'


const API_URL = '/api/';


function App() {
  const [photos, setPhotos] = useState([])
  const [currentIndex, setCurrentIndex] = useState(0)
  const [alertState, setAlertState] = useState({
    show: false,
    message: '',
    variant: '',
  })

  const showAlert = ({message, title, variant='success'}) => {
    setAlertState({title, message, variant, show: true})
  }

  const handleDelete = async lookup => {
    try {
        await fetch(`${API_URL}/${lookup}`, {method: 'DELETE'})
        setPhotos(prevPhotos => prevPhotos.filter(p => p.lookup !== lookup))
        currentIndex >= photos.length - 1 && setCurrentIndex(0)
        showAlert({message: 'Фотография успешно удалена'})
      } catch (err) {
        showAlert({message: `Ошибка удаления фотографии: ${err}`, variant: 'danger'})
      }
  }

  const handleSubmit = async body => {
    try {
      const resp = await fetch(API_URL, {method: 'POST', body})
      const addedPhoto = await resp.json()

      setPhotos(prevPhotos => (
        prevPhotos.some(p => p.lookup === addedPhoto.lookup) ? prevPhotos : (
          setCurrentIndex(photos.length),
          [...prevPhotos, addedPhoto]
        )
      ))
      showAlert({message: 'Фотография успешно добавлена'})
    } catch (err) {
      showAlert({message: `Ошибка загрузки фотографии: ${err}`, variant: 'danger'})
    }
  }

  useEffect(() => {
    fetch(API_URL)
      .then(resp => resp.json())
      .catch(err => showAlert({message: `Ошибка получения фотографий: ${err}`, variant: 'danger'}))
      .then(setPhotos)
  }, [])

  return (
    <>
      <div className="d-flex flex-column min-vh-100">
        <Navbar expand="lg" className="bg-light">
          <Container fluid>
            <Navbar.Brand href="/">Docker Compose Example</Navbar.Brand>
          </Container>
        </Navbar>
        <div className="flex-grow-1 d-flex align-items-stretch">
          <Container fluid>
            <Row className="mt-4">
              <Col>
                <AlertDismissible state={alertState} setState={setAlertState} />
              </Col>
            </Row>
            <Row className="my-4">
              <Col>
                <UploadForm onSubmit={handleSubmit} />
              </Col>
            </Row>
            <Row className="my-4">
              <Col md={{span: 6, offset: 3}}>
                <Gallery
                  photos={photos}
                  activeIndex={currentIndex}
                  onDelete={handleDelete}
                  onSelect={setCurrentIndex}
                />
              </Col>
            </Row>
          </Container>
        </div>
      </div>
    </>
  )
}

export default App
