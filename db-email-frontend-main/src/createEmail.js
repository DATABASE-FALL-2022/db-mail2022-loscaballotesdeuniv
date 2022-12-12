import React, { Component, useState, useEffect } from 'react'
import {Checkbox, Form, Grid, Header, Input, TextArea, Select, Segment, Radio, Image, Icon, Button, Modal} from 'semantic-ui-react'
import {Link, useNavigate} from 'react-router-dom';
import Axios from "axios";

function CreateEmail(){
    const navigate = useNavigate()
    const url = "http://127.0.0.1:5000/loscaballotesdeuniv/emails"
    const [user_id, setUser_ID] = useState('')
    const [ename, setEname] = useState('')
    const [subject, setSubject] = useState('')
    const [body, setBody] = useState('')
    const [emailtype, setEmailType] = useState('')
    const [recipientid, setRecipientID] = useState('')
    const [open, setOpen] = useState(false);

    const options = [
    { key: 't', text: 'To', value: 'To' },
    { key: 'b', text: 'BCC', value: 'BCC' },
    { key: 'c', text: 'CC', value: 'CC' },
]

    console.log(open);
    const handleChange = (event, newValue) => {
        setOpen(true);}

    const navigateToUserView = () => {
        navigate('../loscaballotesdeuniv/UserView');
    };

    const navigateToHome = () => {
        navigate('../loscaballotesdeuniv/Login')
    }

    async function submit() {
        await fetch(url, {
            method: "POST",
            body: JSON.stringify({
                user_id: user_id,
                ename: ename,
                subject: subject,
                body: body,
                emailtype: emailtype,
                recipientid: recipientid,
            }),
            headers: {"Content-Type": "application/json"},
        })
            .then(function (response) {
                if (response.status === 200) {
                    localStorage.setItem("user_id", response.data[0].eid)
                    console.log(localStorage.getItem("eid"))
                }
                console.log(JSON.stringify(response.data));
                console.log('success');
            })
    }

        return (
            <Segment>
                <Header dividing textAlign="center" size="medium">Create Email !
                </Header>
                <Modal
                    centered={false}
                    open={open}
                    onClose={() => setOpen(false)}
                    onOpen={() => setOpen(true)}
                >
                    <Modal.Header>Success!</Modal.Header>
                    <Modal.Content>
                        <Modal.Description>
                            Email has been created successfully! Do you want to send the email?
                        </Modal.Description>
                    </Modal.Content>
                    <Modal.Actions>
                        <Button as={Link} to='/loscaballotesdeuniv/UserView' onClick={() => setOpen(false)}>OK</Button>
                    </Modal.Actions>
                </Modal>

            <Form onSubmit={submit}>
                <Form.Group widths='equal'>
                    <Form.Field
                        required={true}
                        control={Input}
                        label='Enter your User ID'
                        placeholder='User ID'
                        id='user_id'
                        value={user_id}
                        onChange={(e) => {
                            setUser_ID(e.target.value)
                        }}
                    />
                    <Form.Field
                        required={true}
                        control={Input}
                        label='Enter the Recipient ID'
                        placeholder='Recipient ID'
                        id='recipientid'
                        value={recipientid}
                        onChange={(e) => {
                            setRecipientID(e.target.value)
                        }}
                    />
                    <Form.Field
                        required={true}
                        control={Input}
                        label='Enter the Email Type'
                        placeholder='BCC, CC or To'
                        id='emailtype'
                        value={emailtype}
                        onChange={(e) => {
                            setEmailType(e.target.value)
                        }}
                    />
                </Form.Group>
                <Form.Field
                    required={true}
                    control={Input}
                    label='Email Name'
                    placeholder='Email Name'
                    id='ename'
                    value={ename}
                    onChange={(e) => {
                        setEname(e.target.value)
                    }}
                />
                <Form.Field
                    required={true}
                    control={Input}
                    label='Email Subject'
                    placeholder='Email Subject'
                    id='subject'
                    value={subject}
                    onChange={(e) => {
                        setSubject(e.target.value)
                    }}
                />
                <Form.Field
                    required={true}
                    control={TextArea}
                    label='Email Body'
                    placeholder='Start writing :)'
                    id='body'
                    value={body}
                    onChange={(e) => {
                        setBody(e.target.value)
                    }}
                />
                <Form.Button content='Submit' primary onClick={handleChange}/>
            </Form>
            </Segment>
        )
}

export default CreateEmail;
