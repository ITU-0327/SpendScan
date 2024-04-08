import React, { Component } from "react";
import { render } from "react-dom";
import HomePage from "./HomePage";
import RoomJoinPage from "./RoomJoinPage";
import RoomCreatePage from "./RoomCreatePage";

//import { data } from "./data";
//import { Sankey } from "./Sankey";

export default class App extends Component {
    constructor(props){
        super(props);
    }

    render(){
    return(
    <div>
        <HomePage />
        <RoomJoinPage />
        <RoomCreatePage />
    </div>

    );

//        return <HomePage />
//        return <h1>Testing React Code {this.props.name}</h1>;
    }
}

const appDiv = document.getElementById("app");
render(<App name="bob"/>, appDiv);
//ReactDOM.render(<Sankey data={data} width={400} height={400} />, appDiv)