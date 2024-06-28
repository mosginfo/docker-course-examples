import 'bootstrap/dist/css/bootstrap.min.css'
import {
  useEffect,
  useRef,
  useState,
} from 'react'
import {
  Button,
  Carousel,
  Col,
  Container,
  Form,
  InputGroup,
  Navbar,
  Row,
} from 'react-bootstrap'


const API_URL = '/api/';


function UploadForm({ onSubmit }) {
  const handleSubmit = async e => {
    e.preventDefault()
    const formData = new FormData(e.target)
    onSubmit && onSubmit(formData)
  }

  return (
    <Form onSubmit={handleSubmit}>
      <InputGroup>
        <Form.Control type="file" name="file" />
        <Button type="submit">Submit</Button>
      </InputGroup>
    </Form>
  )
}

function Gallery({ photos, onDelete, ...carouselProps }) {
  const handleClickDelete = e => {
    if (event.target && event.target.dataset.action === 'delete') {
      const lookup = event.target.dataset.lookup
      onDelete && onDelete(lookup)
    }
  }

  const slides = photos.map(photo => (
    <Carousel.Item key={photo.lookup}>
      <img src={photo.url} className="d-block w-100" alt="" />
      <Carousel.Caption>
        <Button variant="danger" data-action="delete" data-lookup={photo.lookup}>Delete</Button>
      </Carousel.Caption>
    </Carousel.Item>
  ));

  return (
    <Carousel onClick={handleClickDelete} {...carouselProps}>
      {slides}
    </Carousel>
  )
}


function App() {
  const [photos, setPhotos] = useState([])
  const [currentIndex, setCurrentIndex] = useState(0)

  const handleDelete = async lookup => {
    try {
        await fetch(`${API_URL}/${lookup}`, {method: 'DELETE'})
        setPhotos(prevPhotos => prevPhotos.filter(p => p.lookup !== lookup))
        currentIndex >= photos.length - 1 && setCurrentIndex(0)
      } catch (error) {
        console.error('Error deleting photo:', error)
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
    } catch (err) {
      console.error('Error uploading photo:', err)
    }
  }

  useEffect(() => {
    fetch(API_URL)
      .then(resp => resp.json())
      .catch(err => console.error('Error fetching photos:', err))
      .then(data => setPhotos(data.files))
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
