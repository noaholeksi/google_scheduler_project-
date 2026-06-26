import React, { Component } from 'react';
import styled from 'styled-components';
import { RecurringForm, CommitmentForm, DailyForm, DeadlineForm, HobbyForm} from './activity_forms';
import MyActivities from './my_activities';
import ScheduleMaker from './schedule_maker';

const Container = styled.div`
  display: flex;
  width: 100vw;
  height: 100vh;
`;

const LeftSection = styled.div`
  flex: 3;
  background-color: lightblue;
  padding: 20px;
`;

const MiddleSection = styled.div`
  flex: 5;
  background-color: lightcoral;
  padding: 20px;
`;

const RightSection = styled.div`
  flex: 2;
  background-color: right;
  padding: 20px;
  `;

class NewActivityMaker extends Component{
    constructor(props) {
        super(props);
        this.state = {
          selectedActivityType: 'Commitment' // Initialize state to store the selected fruit
        };
      }
    
      // Handle change event when a radio button is selected
      //state is managed within the component itself
      handleChange = (event) => {
        this.setState(
            { selectedActivityType: event.target.value },
             () => {
          console.log(this.state.selectedActivityType); // Output the selected ActivityType to the console
        });
      };
      render() {
        const { selectedActivityType } = this.state;

        return (
        <div>
          <form>
              <input
                type="radio"
                id="recurring"
                name="ActivityType"
                value="Recurring"
                checked={this.state.selectedActivityType === 'Recurring'}
                onChange={this.handleChange}
              />
              <label htmlFor="recurring">Recurring</label>
            
              <input
                type="radio"
                id = "commitment"
                name="ActivityType"
                value="Commitment"
                checked={this.state.selectedActivityType === 'Commitment'}
                onChange={this.handleChange}
              />
              <label htmlFor="commitment">Commitment</label>

              <input
                type="radio"
                id="daily"
                name="ActivityType"
                value="Daily"
                checked={this.state.selectedActivityType === 'Daily'}
                onChange={this.handleChange}
              />
              <label htmlFor="daily">Daily</label>

              <input
                type="radio"
                id="deadline"
                name="ActivityType"
                value="Deadline"
                checked={this.state.selectedActivityType === 'Deadline'}
                onChange={this.handleChange}
              />
              <label htmlFor="deadline">Deadline</label>

              <input
                type="radio"
                id="hobby"
                name="ActivityType"
                value="Hobby"
                checked={this.state.selectedActivityType === 'Hobby'}
                onChange={this.handleChange}
              />
              <label htmlFor="hobby">Hobby/Chore</label>
          </form>

          <br/>
          {selectedActivityType === 'Recurring' &&(
          <RecurringForm/>
          )}
          {selectedActivityType === 'Commitment' &&(
          <CommitmentForm/>
          )}
          {selectedActivityType === 'Daily' &&(
          <DailyForm/>
          )}
          {selectedActivityType === 'Deadline' &&(
          <DeadlineForm/>
          )}
          {selectedActivityType === 'Hobby' &&(
          <HobbyForm/>
          )}
        </div>

        );
      }

}




class App extends Component {
    render(){  
    return (
    <Container>
      <LeftSection>
        <MyActivities/>
      </LeftSection>
      <MiddleSection>
        <NewActivityMaker/>  
      </MiddleSection>
      <RightSection>
        <ScheduleMaker/>
      </RightSection>
    </Container>
   );
 }
}

export default App;
