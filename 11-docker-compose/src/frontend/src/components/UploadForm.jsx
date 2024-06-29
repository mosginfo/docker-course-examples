import {
  Button,
  Form,
  InputGroup,
} from 'react-bootstrap'


export default function({ onSubmit }) {
  const handleSubmit = async e => {
    e.preventDefault()
    const formData = new FormData(e.target)
    onSubmit && onSubmit(formData)
  }

  return (
    <Form onSubmit={handleSubmit}>
      <InputGroup>
        <Form.Control type="file" name="file" required />
        <Button type="submit">Submit</Button>
      </InputGroup>
    </Form>
  )
}
