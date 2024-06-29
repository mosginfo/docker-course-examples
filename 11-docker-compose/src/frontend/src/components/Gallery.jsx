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


export default function({ photos, onDelete, ...carouselProps }) {
  const DateTime = ({ dateString }) => {
    const dt = new Date(dateString)
    const options = {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: 'numeric',
      minute: 'numeric',
    }
    return <>{dt.toLocaleDateString(undefined, options)}</>
  }

  const handleClickDelete = e => {
    if (event.target && event.target.dataset.action === 'delete') {
      const lookup = event.target.dataset.lookup
      onDelete && onDelete(lookup)
    }
  }

  const slides = photos.map(photo => (
    <Carousel.Item key={photo.id}>
      <img src={photo.url} className="d-block w-100" alt="" />
      <Carousel.Caption>
        <p><DateTime dateString={photo.created} /></p>
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
