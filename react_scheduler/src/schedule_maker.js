import React, { Component } from 'react';
import axios from 'axios';


class ScheduleMaker extends (Component){

    handleClick = (event) => {
        event.preventDefault();
        axios.put('http://localhost:5001/api/schedulers/authorize')
          .then(response => {
            console.log(response.data); // Handle success, e.g., show a success message
          })
          .catch(error => {
            console.error('Error saving data:', error); // Handle error, e.g., show an error message
          });;
    }

    render() {
        return (
            <div>
                Press submit to genererate your schedule
                <button onClick={this.handleClick}>Generate Schedule</button>

            </div>
        )
    }
}

export default ScheduleMaker;