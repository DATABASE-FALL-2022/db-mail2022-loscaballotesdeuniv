import React, {Component, useState} from 'react';
import {Button, Card, Container, Divider, Header, Icon, Image, Modal, Tab} from "semantic-ui-react";
import Dashboard from "./Dashboard";
import Emails from "./Emails";
import CreateEmail from "./createEmail";

function UserView(){
    const [isAuth, setIsAuth] = useState(true)
    const [notShow, setNotShow] = useState(false)
    const panes = [
        {
            menuItem: 'Profile', render: () => <Tab.Pane active={isAuth}>:) <Card>
                <Card.Content>
                    <Card.Header>Matthew</Card.Header>
                    <Card.Meta>
                        <span className='date'>Joined in 2015</span>
                    </Card.Meta>
                    <Card.Description>
                        Matthew is a musician living in Nashville.
                    </Card.Description>
                </Card.Content>
                <Card.Content extra>
                    <a>
                        <Icon name='user' />
                        22 Friends
                    </a>
                </Card.Content>
            </Card></Tab.Pane>
        },
        {
            menuItem: 'Friend List', render: () => <Tab.Pane active={isAuth}><Dashboard/></Tab.Pane>
        },
        {
            menuItem: 'Inbox', render: () => <Tab.Pane active={isAuth}><Container><Header>Anything you need to put here</Header><Divider/></Container><Emails/></Tab.Pane>
        },
        {
            menuItem: 'Outbox', render: () => <Tab.Pane active={isAuth}><Container><Header>Anything you need to put here</Header><Divider/></Container><Emails/></Tab.Pane>
        },
        {
            menuItem: 'Favorites', render: () => <Tab.Pane active={isAuth}><Container><Header>Anything you need to put here</Header><Divider/></Container><Emails/></Tab.Pane>
        },
        {
            menuItem: 'Deleted', render: () => <Tab.Pane active={isAuth}><Container><Header>Anything you need to put here</Header><Divider/></Container><Emails/></Tab.Pane>
        },
        {
            menuItem: 'Drafts', render: () => <Tab.Pane active={isAuth}><Container><Header>Anything you need to put here</Header><Divider/></Container><Emails/></Tab.Pane>
        },
        {
            menuItem: 'Dashboard', render: () => <Tab.Pane active={isAuth}><Dashboard/></Tab.Pane>
        },
        {
            menuItem: 'Create Email', render: () => <Button active={isAuth}><CreateEmail/></Button>
        },
    ]

    return <Tab panes={panes}/>

}
export default UserView;
