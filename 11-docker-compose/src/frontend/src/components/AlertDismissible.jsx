import { Alert } from 'react-bootstrap'


export default function({ state, setState }) {
  return (
    <>
      {state.show && (
        <Alert variant={state.variant} onClose={() => setState({ ...state, show: false })} dismissible>
          {state.title && <Alert.Heading>{state.title}</Alert.Heading>}
          {state.message && <p className="m-0">{state.message}</p>}
        </Alert>
      )}
    </>
  )
}
