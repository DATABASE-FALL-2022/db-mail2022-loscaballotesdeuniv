import React from 'react'
import { Button, Form } from 'semantic-ui-react'

const SignUp = () => (
    <Form>
        <Form.Group unstackable widths={2}>
            <Form.Input label='First name' placeholder='First name' />
            <Form.Input label='Last name' placeholder='Last name' />
        </Form.Group>
        <Form.Group widths={2}>
            <Form.Input label='Date of Birth' placeholder='mm/dd/yyyy' />
            <Form.Input label='Phone' placeholder='Phone' />
        </Form.Group>
        <Form.Group widths={2}>
            <Form.Input label='Email' placeholder='Email' />
            <Form.Input label='Password' placeholder='Password' type='password' />
        </Form.Group>
        <Button type='submit'>Submit</Button>
    </Form>
)

export default SignUp