import React, {Component, useState} from 'react';
import {Button, Card, Container, List, Modal, SegmentGroup, Tab} from "semantic-ui-react";
import AllEmails from "./AllEmails";

function Emails() {
    const [data, setData] = useState("show");
    let random_info = [{"subject": "p1", "content": "la vida y sus complications", "stuff": "description"},
        {"subject": "p2", "content": "la vida y sus complications", "stuff": "description"},
        {"subject": "p3", "content": "la vida y sus complications", "stuff": "description"},
        {"subject": "p44", "content": "la vida y sus complications", "stuff": "description"},
        {"subject": "p456", "content": "la vida y sus complications", "stuff": "description"},
        {"subject": "pas", "content": "la vida y sus complications", "stuff": "description"},
        {"subject": "p1asdf", "content": "la vida y sus complications", "stuff": "description"},
        {"subject": "p1asdfdf", "content": "la vida y sus complications", "stuff": "description"},
        {"subject": "p1asdfedee", "content": "la vida y sus complications", "stuff": "description"},
        {"subject": "pvdvs1", "content": "la vida y sus complications", "stuff": "description"},
        {"subject": "fsdfp1", "content": "la vida y sus complications", "stuff": "description"},
        {"subject": "psdf1", "content": "la vida y sus complications", "stuff": "description"},
        {"subject": "p1dfseef", "content": "la vida y sus complications", "stuff": "description"},
        {"subject": "YAAAAAA", "content": "la vida y sus complications", "stuff": "description"},
        {"subject": "p1d", "content": "la vida y sus complications", "stuff": "description"},
        {"subject": "-.-", "content": "la vida y sus complications", "stuff": "description"},
        {"subject": "ahhhhh", "content": "la vida y sus complications", "stuff": "description"},
        {"subject": "byeeeee", "content": "la vida y sus complications", "stuff": "description"}];


    return <SegmentGroup>
        <AllEmails info={random_info}/>
    </SegmentGroup>
}

export default Emails;