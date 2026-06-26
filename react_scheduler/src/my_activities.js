import React, { Component } from 'react';
import styled from 'styled-components';
import axios from 'axios';
import { RecurringForm, CommitmentForm, DailyForm, DeadlineForm, HobbyForm} from './activity_forms';

const ScrollContainer = styled.div`
max-height: 200px;
overflow-y: auto;
border: 1px solid;
padding: 10px;
`;


class MyActivities extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: [],
      error: null,
      //name:"",
      selectedActivity: {},
      //x:0
    };
  }

  componentDidMount() {
    this.fetchActivities();
  }

  fetchActivities = async () => {
    try {
      const response = await axios.get('http://localhost:5001/api/schedulers/myActivities');
      this.setState({ data: response.data });
    } catch (error) {
      console.error('Error fetching the activities:', error);
      this.setState({ error: error.message });
    }
  }

  handleDelete = (event) => {
        event.preventDefault();
    const name = this.state.selectedActivity.name;
    console.log(name);
    axios.delete('http://localhost:5001/api/schedulers/' + name)
        .then(response => {
          console.log(response.data); // Handle success, e.g., show a success message
        })
        .catch(error => {
          console.error('Error saving data:', error); // Handle error, e.g., show an error message
        });
}

  handleChange = (event) =>{

    //this.setState({selectedActivity:  null});
    this.setState({selectedActivity:  JSON.parse(event.target.value)});
  };

  //changing the name and pressing submit will not alter the current but will create a new activity

  render() {
    const { data, error, selectedActivity,x } = this.state;
    return (
      <div>
        <h1>Your Activities</h1>
        {error && <p>Error: {error}</p>}
        <ScrollContainer>
          {data.map((activity, index) => (//array.map(element, index) is the form
            // <li key={index}>{activity.name}</li>
            <div>
            <input 
              type="radio"
              id={`activity-${index}`}
              name="activity"
              key={index}
              value={JSON.stringify(activity)}
              checked = {this.state.selectedActivity.name === activity.name}
              onChange={this.handleChange}
            />
            <label htmlFor={`activity-${index}`}>{activity.name}</label>
            </div>
          ))}
        </ScrollContainer>


        {selectedActivity && selectedActivity.type === 're' &&(
          <RecurringForm 
          initNameInput={selectedActivity.name}/>
        )}
        {selectedActivity && selectedActivity.type === 'co' &&(
          <CommitmentForm 
          name={selectedActivity.name}
          date={selectedActivity.date}
          start={selectedActivity.start}
          end={selectedActivity.end}
          also_accomplishes={selectedActivity.also_accomplishes}/>
        )}
        {selectedActivity && selectedActivity.type === 'da'  && (
          <DailyForm
          name = {selectedActivity.name}
          start={selectedActivity.start}
          end={selectedActivity.end}
          min_hours={selectedActivity.min_hours}
          max_hours={selectedActivity.max_hours}/>
        )}
        {selectedActivity && selectedActivity.type === 'de'  &&(
          <DeadlineForm
          name = {selectedActivity.name}
          date={selectedActivity.date}
          hours_left = {selectedActivity.hours_left}
          min_hours={selectedActivity.min_hours}
          max_hours={selectedActivity.max_hours}
          />
        )}
        {selectedActivity && selectedActivity.type === 'ho'  &&(
          <HobbyForm
          name = {selectedActivity.name}
          frequency = {selectedActivity.frequency}
          date={selectedActivity.date}
          hours_left = {selectedActivity.hours_left}
          min_hours={selectedActivity.min_hours}
          max_hours={selectedActivity.max_hours}
          start={selectedActivity.start}
          end={selectedActivity.end}
          />
        )}
        <button onClick={this.handleDelete}>Delete Activity</button>
      </div>// add a delete button
    );
  }
}

export default MyActivities;
