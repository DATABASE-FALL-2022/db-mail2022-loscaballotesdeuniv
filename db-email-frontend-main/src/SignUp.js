// import { Button, Form } from 'semantic-ui-react'
// import React, { useState, useEffect } from "react";
//
// function  SignUp() {
//     const [data, setData] = useState([]);
//     const [inputs, setInputs] = useState({});
//
//     //Get Method
//     const apiGet = () => {
//         fetch("http://127.0.0.1:5000/loscaballotesdeuniv/users")
//             .then((response) => response.json())
//             .then((json) => {
//                 console.log(json);
//                 setData(json);
//             });
//     };
//
//     //Post Method
//     const apiPost = async () => {
//         await fetch("http://127.0.0.1:5000/loscaballotesdeuniv/users", {
//             method: "POST",
//             form : JSON.stringify({
//                 firstname: inputs.firstname,
//                 lastname: inputs.lastname,
//                 date_of_birth: inputs.date_of_birth,
//                 email: inputs.email,
//                 password: inputs.password,
//                 phone_number: inputs.phone_number,
//             }),
//         })
//             .then((response) => response.json())
//             .then((json) => console.log(json));
//     };
//
//     const handleChange = (event) => {
//         event.persist();
//         setInputs((inputs) => ({
//             ...inputs,
//
//             [event.target.name]: event.target.value,
//         }));
//     };
//
//     const handleSubmit = (event) => {
//         event.preventDefault();
//         apiPost();
//         console.log(inputs);
//     };
//
//       // useEffect(() => {
//       //   apiGet();
//       // }, []);
//
//
//     return (
//         <div>
//             My API <br />
//             <button onClick={apiGet}>Fetch API</button>
//             <br />
//         <Form onSubmit={handleSubmit}>
//             <ul>
//                 {data.map((item) => (
//                     <li key={item.id}>
//                         {item.firstname},{item.lastname},{item.date_of_birth},{item.phone_number},{item.email},{item.password}
//                     </li>
//                 ))}
//             </ul>
//             <Form.Group unstackable widths={2}>
//                 <Form.Input type="text" name="firstname" label='First name' placeholder='First name' onChange={handleChange} />
//                 <Form.Input type="text" name="lastname" label='Last name' placeholder='Last name' onChange={handleChange} />
//             </Form.Group>
//             <Form.Group widths={2}>
//                 <Form.Input type="text" name="date_of_birth" label='Date of Birth' placeholder='mm/dd/yyyy' onChange={handleChange} />
//                 <Form.Input type="text" name="phone_number" label='Phone' placeholder='Phone' onChange={handleChange} />
//             </Form.Group>
//             <Form.Group widths={2}>
//                 <Form.Input type="text" name="email" label='Email' placeholder='Email' onChange={handleChange} />
//                 <Form.Input name="password" label='Password' placeholder='Password' type='password' onChange={handleChange} />
//             </Form.Group>
//             <input type="submit" value="Submit" onChange={apiPost} />
//         </Form>
//         </div>
//     );
// }
//
// export default  SignUp;

import React, { Component, useState, useEffect } from 'react'
import {Checkbox, Form, Grid, Header, Segment, Radio, Image, Icon, Button, Modal} from 'semantic-ui-react'
import {Link, useNavigate} from 'react-router-dom';
import Axios from "axios";

function SignUp(){
    const navigate = useNavigate()
    const url = "http://127.0.0.1:5000/loscaballotesdeuniv/users"
    const [firstName, setFirstName] = useState('')
    const [lastName, setLastName] = useState('')
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [phone_number, setPhoneNumber] = useState('')
    const [date_of_birth, setDateOfBirth] = useState('')
    const [open, setOpen] = useState(false);
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
                firstname: firstName,
                lastname: lastName,
                email: email,
                password: password,
                phone_number: phone_number,
                date_of_birth: date_of_birth,
            }),
            headers: {"Content-Type": "application/json"},
        })
            .then(async () => {
                let email = email
                let data = JSON.stringify({
                    "email": email,
                    "password": password
                });

                let config = {
                    method: 'post',
                    url: '/loscaballotesdeuniv/users',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    data: data
                };
                Axios(config)
                    .then(function (response) {
                        if (response.status === 200) {
                            localStorage.setItem("user_id", response.data[0].user_id)
                            console.log(localStorage.getItem("user_id"))
                        }
                        console.log(JSON.stringify(response.data));
                        console.log('success');
                    })
                    .catch(function (error) {
                        console.log(error);
                        let message = typeof error.response !== "undefined" ? error.response.data.message : error.message;
                        console.warn("Email address does not exist", message);
                    });
            })
            .then(navigateToUserView)
    }

    return (
        <Segment>
            <Header dividing textAlign="center" size="huge">Sign Up to RUMail
                <Image size='mini'/>
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
                        Sign Up has been successful.
                    </Modal.Description>
                </Modal.Content>
                <Modal.Actions>
                    <Button as={Link} to='/loscaballotesdeuniv/login' onClick={() => setOpen(false)}>OK</Button>
                </Modal.Actions>
            </Modal>
            <Segment placeholder>

                <Form onSubmit={submit}>
                    <Button icon floated='left' onClick={navigateToHome}>
                        <Icon name='arrow circle left'/> Back To Login
                    </Button>
                    <Form.Input
                        required={true}
                        label='First Name'
                        placeholder='First Name'
                        id='firstname'
                        value={firstName}
                        onChange={(e) => {
                            setFirstName(e.target.value)
                        }}
                    />
                    <Form.Input
                        required={true}
                        label='Last Name'
                        placeholder='Last Name'
                        id='lastname'
                        value={lastName}
                        onChange={(e) => {
                            setLastName(e.target.value)
                        }}

                    />
                    <Form.Input
                        required={true}
                        label='Email'
                        placeholder='username@rumail.com'
                        id='username'
                        value={email}
                        onChange={(e) => {
                            setEmail(e.target.value)
                        }}
                    />
                    <Form.Input
                        required={true}
                        label='Password'
                        placeholder='Password'
                        type='password'
                        id='password'
                        value={password}
                        onChange={(e) => {
                            setPassword(e.target.value)
                        }}
                    />
                    <Form.Input
                        required={true}
                        label='Phone Number'
                        placeholder='Phone Number'
                        id='phone_number'
                        value={phone_number}
                        onChange={(e) => {
                            setPhoneNumber(e.target.value)
                        }}
                    />
                    <Form.Input
                        required={true}
                        label='Date Of Birth'
                        placeholder='mm/dd/yyyy'
                        id='date_of_birth'
                        value={date_of_birth}
                        onChange={(e) => {
                            setDateOfBirth(e.target.value)
                        }}
                    />
                    <Form.Button content='Submit' primary onClick={handleChange}/>
                </Form>
            </Segment>
        </Segment>
    )
}

export default SignUp;