import React, { Component } from 'react';
import axios from 'axios'



//import styled from 'styled-components';

class RecurringForm extends Component{
  constructor(props) {
      super(props);
      this.state = {
        nameInput: props.name || '' ,// Initialize states 
        daysTF:[false, false, false, false, false, false, false],
        timesGrid:[['',''],['',''],['',''],['',''],['',''],['',''],['','']]
      };
  }
      
      updateName = (event) => {
        this.setState({nameInput:event.target.value});
      };
      
      handleMonChange = (event) => {
        const updatedDaysTF = [...this.state.daysTF];
        updatedDaysTF[0] = event.target.checked;
        this.setState({ daysTF: updatedDaysTF });
      };
      updateMonTime1 = (event) => {
        const updatedTimesGrid = [...this.state.timesGrid];
        updatedTimesGrid[0][0] = event.target.value; 
        this.setState({ timesGrid: updatedTimesGrid });
      }; 
      updateMonTime2 = (event) => {
        const updatedTimesGrid = [...this.state.timesGrid];
        updatedTimesGrid[0][1] = event.target.value; 
        this.setState({ timesGrid: updatedTimesGrid });
      }; 
      handleTueChange = (event) => {
        const updatedDaysTF = [...this.state.daysTF];
        updatedDaysTF[1] = event.target.checked;
        this.setState({ daysTF: updatedDaysTF });
      };
      updateTueTime1 = (event) => {
        const updatedTimesGrid = [...this.state.timesGrid];
        updatedTimesGrid[1][0] = event.target.value; 
        this.setState({ timesGrid: updatedTimesGrid });
      }; 
      updateTueTime2 = (event) => {
        const updatedTimesGrid = [...this.state.timesGrid];
        updatedTimesGrid[1][1] = event.target.value; 
        this.setState({ timesGrid: updatedTimesGrid });
      }; 
      handleWedChange = (event) => {
        const updatedDaysTF = [...this.state.daysTF];
        updatedDaysTF[2] = event.target.checked;
        this.setState({ daysTF: updatedDaysTF });
      };
      updateWedTime1 = (event) => {
        const updatedTimesGrid = [...this.state.timesGrid];
        updatedTimesGrid[2][0] = event.target.value; 
        this.setState({ timesGrid: updatedTimesGrid });
      }; 
      updateWedTime2 = (event) => {
        const updatedTimesGrid = [...this.state.timesGrid];
        updatedTimesGrid[2][1] = event.target.value; 
        this.setState({ timesGrid: updatedTimesGrid });
      }; 
      handleThuChange = (event) => {
        const updatedDaysTF = [...this.state.daysTF];
        updatedDaysTF[3] = event.target.checked;
        this.setState({ daysTF: updatedDaysTF });
      };
      updateThuTime1 = (event) => {
        const updatedTimesGrid = [...this.state.timesGrid];
        updatedTimesGrid[3][0] = event.target.value; 
        this.setState({ timesGrid: updatedTimesGrid });
      }; 
      updateThuTime2 = (event) => {
        const updatedTimesGrid = [...this.state.timesGrid];
        updatedTimesGrid[3][1] = event.target.value; 
        this.setState({ timesGrid: updatedTimesGrid });
      }; 
      handleFriChange = (event) => {
        const updatedDaysTF = [...this.state.daysTF];
        updatedDaysTF[4] = event.target.checked;
        this.setState({ daysTF: updatedDaysTF });
      };
      updateFriTime1 = (event) => {
        const updatedTimesGrid = [...this.state.timesGrid];
        updatedTimesGrid[4][0] = event.target.value; 
        this.setState({ timesGrid: updatedTimesGrid });
      }; 
      updateFriTime2 = (event) => {
        const updatedTimesGrid = [...this.state.timesGrid];
        updatedTimesGrid[4][1] = event.target.value; 
        this.setState({ timesGrid: updatedTimesGrid });
      }; 
      handleSatChange = (event) => {
        const updatedDaysTF = [...this.state.daysTF];
        updatedDaysTF[5] = event.target.checked;
        this.setState({ daysTF: updatedDaysTF });
      };
      updateSatTime1 = (event) => {
        const updatedTimesGrid = [...this.state.timesGrid];
        updatedTimesGrid[5][0] = event.target.value; 
        this.setState({ timesGrid: updatedTimesGrid });
      }; 
      updateSatTime2 = (event) => {
        const updatedTimesGrid = [...this.state.timesGrid];
        updatedTimesGrid[5][1] = event.target.value; 
        this.setState({ timesGrid: updatedTimesGrid });
      }; 

      handleSunChange = (event) => {
        const updatedDaysTF = [...this.state.daysTF];
        updatedDaysTF[6] = event.target.checked;
        this.setState({ daysTF: updatedDaysTF });
      };
      //state values are immutble, so you must create a copy, alter the copy, then assign the value of the original to the altered copy
      updateSunTime1 = (event) => { 
        const updatedTimesGrid = [...this.state.timesGrid];
        updatedTimesGrid[6][0] = event.target.value; 
        this.setState({ timesGrid: updatedTimesGrid });
      }; 
      updateSunTime2 = (event) => {
        const updatedTimesGrid = [...this.state.timesGrid];
        updatedTimesGrid[6][1] = event.target.value; 
        this.setState({ timesGrid: updatedTimesGrid });
      }; 

      handleSubmit = (event) =>{
        event.preventDefault();
        //const days = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]
        const times = this.state.timesGrid;
        const daysTF = this.state.daysTF;
        let daysString = '';
        let timesString = '';
        for(let i = 0; i< daysTF.length; i++){
           // strict equality comparison without type conversion
          if (daysTF[i] == true){
            daysString += i + " ";
            timesString  += times[i][0] + "-" + times[i][1] + " ";
          }
        }
        daysString = daysString.slice(0, -1); // removes the last character which should be a space
        timesString = timesString.slice(0, -1);
        let dataList  = [1, this.state.nameInput, daysString, timesString];
        let data = {
          name: this.state.nameInput,
          type: "re",
          week_days: daysString,
          time_pairs: timesString
        };
        axios.post('http://localhost:5001/api/schedulers/myActivities', data)
            .then(response => {
              console.log(response.data); // Handle success, e.g., show a success message
            })
            .catch(error => {
              console.error('Error saving data:', error); // Handle error, e.g., show an error message
            });
      };


    
  
  
    // Handle change event when a radio button is selected
    //state is managed within the component itself
    
    render() {
      const { mon, tue, wed, thu, fri, sat, sun } = this.state;

      return (
        <div>
        <div>Please enter the info for creating your Recurring Activity</div>
        <br/>
        <form onSubmit={this.handleSubmit}>
          Name&nbsp;
          <input
            type="text"
            id="title"
            value={this.state.nameInput}
            onChange={this.updateName}
          />
          <br/>
          Select the days this activity recurs on 
          <br/>
           Monday&nbsp;
          <input
            type="checkbox"
            id="monday"
            checked={this.state.daysTF[0] === true}
            onChange={this.handleMonChange}
          /> 
           | Tuesday&nbsp;
          <input
            type="checkbox"
            id="tuesday"
            checked={this.state.daysTF[1] === true}
            onChange={this.handleTueChange}
          /> 
           | Wednesday&nbsp;
          <input
            type="checkbox"
            id="wednesday"
            checked={this.state.daysTF[2]=== true}
            onChange={this.handleWedChange}
          />
          | Thursday&nbsp;
          <input
            type="checkbox"
            id="thursday"
            checked={this.state.daysTF[3] === true}
            onChange={this.handleThuChange}
          />  
          | Friday&nbsp;
          <input
            type="checkbox"
            id="friday"
            checked={this.state.daysTF[4] === true}
            onChange={this.handleFriChange}
          />
          | Saturday&nbsp;
          <input
            type="checkbox"
            id="saturday"
            checked={this.state.daysTF[5] === true}
            onChange={this.handleSatChange}
          />
          | Sunday&nbsp;
          <input
            type="checkbox"
            id="sunday"
            checked={this.state.daysTF[6] === true}
            onChange={this.handleSunChange}
          /> 
          <br/>

          {this.state.daysTF[6] === true  &&(
            <>
            <label>Sunday start and end time </label>
            <input 
             type="time"
              id="sunT1"
              value={this.state.timesGrid[6][0]}
              onChange={this.updateSunTime1}
            />

            <input 
              type="time"
              id="sunT2"
              value={this.state.timesGrid[6][1]}
              onChange={this.updateSunTime2}
            />
            <br/>
            </>
          )
          }
          {this.state.daysTF[0] === true  &&(
            <>
            <label>Monday start and end time </label>
            <input 
             type="time"
              id="monT1"
              value={this.state.timesGrid[0][0]}
              onChange={this.updateMonTime1}
            />

            <input 
              type="time"
              id="monT2"
              value={this.state.timesGrid[0][1]}
              onChange={this.updateMonTime2}
            />
            <br/>
            </>
          )
          }

          {this.state.daysTF[1] === true  &&(
            <>
            <label>Tuesday start and end time </label>
            <input 
             type="time"
              id="tueT1"
              value={this.state.timesGrid[1][0]}
              onChange={this.updateTueTime1}
            />

            <input 
              type="time"
              id="tueT2"
              value={this.state.timesGrid[1][1]}
              onChange={this.updateTueTime2}
            />
            <br/>
            </>
          )
          }

          {this.state.daysTF[2]=== true  &&(
            <>
            <label>Wedsday start and end time </label>
            <input 
             type="time"
              id="wedT1"
              value={this.state.timesGrid[2][0]}
              onChange={this.updateWedTime1}
            />

            <input 
              type="time"
              id="wedT2"
              value={this.state.timesGrid[2][1]}
              onChange={this.updateWedTime2}
            />
            <br/>
            </>
          )
          }

          {this.state.daysTF[3] === true  &&(
            <>
            <label>Thusday start and end time </label>
            <input 
             type="time"
              id="thuT1"
              value={this.state.timesGrid[3][0]}
              onChange={this.updateThuTime1}
            />

            <input 
              type="time"
              id="thuT2"
              value={this.state.timesGrid[3][1]}
              onChange={this.updateThuTime2}
            />
            <br/>
            </>
          )
          }

            {this.state.daysTF[4] === true  &&(
            <>
            <label>Frisday start and end time </label>
            <input 
             type="time"
              id="friT1"
              value={this.state.timesGrid[4][0]}
              onChange={this.updateFriTime1}
            />

            <input 
              type="time"
              id="friT2"
              value={this.state.timesGrid[4][1]}
              onChange={this.updateFriTime2}
            />
            <br/>
            </>
          )
          }

          {this.state.daysTF[5] === true  &&(
            <>
            <label>Saturday start and end time </label>
            <input 
             type="time"
              id="satT1"
              value={this.state.timesGrid[5][0]}
              onChange={this.updateSatTime1}
            />

            <input 
              type="time"
              id="satT2"
              value={this.state.timesGrid[5][1]}
              onChange={this.updateSatTime2}
            />
            <br/>
            </>
          )
          }
          
          <button type="submit">Submit</button>
        </form>
      </div>

      );
    }

}

class CommitmentForm extends Component{
    constructor(props) {
        super(props);
        this.state = {
          nameInput: props.name || '' ,// Initialize states 
          dateInput: props.date || '',
          //maybe change to start and end as thats what they are in the database
          time1Input: props.start || '',
          time2Input: props.end || '',
          alsoAccomplishesInput: props.alsoAccomplishes || 'N/A'
        };
      }

        updateName = (event) => {
          this.setState({nameInput:event.target.value});
        };
        updateDate= (event) => {
          this.setState({dateInput:event.target.value});
        };
        updateTime1 = (event) => {
          this.setState({time1Input:event.target.value});
        }; 
        updateTime2 = (event) => {
          this.setState({time2Input:event.target.value});
        }; 
        updateAlsoAccomplishes = (event) => {
          this.setState({alsoAccomplishesInput: event.target.value})
        }
        handleSubmit = (event) =>{
          event.preventDefault();
          //let dataList  = [ 2, this.state.nameInput, this.state.dateInput, this.state.time1Input, this.state.time2Input, this.state.alsoAccomplishesInput];
          let data = {
            name: this.state.nameInput,
            type: "co",
            date: this.state.dateInput, 
            start: this.state.time1Input, 
            end: this.state.time2Input, 
            also_accomplishes: this.state.alsoAccomplishesInput
          };
          axios.post('http://localhost:5001/api/schedulers/myActivities', data)
            .then(response => {
              console.log(response.data); // Handle success, e.g., show a success message
            })
            .catch(error => {
              console.error('Error saving data:', error); // Handle error, e.g., show an error message
            });
        };
  


      
    
    
      // Handle change event when a radio button is selected
      //state is managed within the component itself
      
      render() {

        return (
          <div>
          <div>Please enter the info for creating your commitment</div>
          <br/>
          <form onSubmit={this.handleSubmit}>
            Name&nbsp;
            <input
              type="text"
              id="title"
              value={this.state.nameInput}
              onChange={this.updateName}
            />
            <br/>
            Date&nbsp;
            <input
              type="date"
              id="date"
              value={this.state.dateInput}
              onChange={this.updateDate}
            />
            <br/>
            Start time&nbsp;
            <input
              type="time"
              id="time1"
              value={this.state.time1Input}
              onChange={this.updateTime1}
            />
            <br/>
            End time&nbsp;
            <input
              type="time"
              id="time2"
              value={this.state.time2Input}
              onChange={this.updateTime2}
            />
            <br/>
            What other activities will this accomplish&nbsp;
            <input
              type="text"
              id="alsoAccomplishes"
              value={this.state.alsoAccomplishesInput}
              onChange={this.updateAlsoAccomplishes}
            />
            <br/>
            <button type="submit">Submit</button>
          </form>
        </div>

        );
      }

}

class DailyForm extends Component{
  constructor(props) {
      super(props);
      this.state = {
        nameInput: props.name || '' ,// Initialize states 
        time1Input: props.start || '',
        time2Input: props.end || '',
        //change to minlength and max length
        minLengthInput: props.min_hours || '',
        maxLengthInput: props.max_hours || ''
      };
    }

      updateName = (event) => {
        this.setState({nameInput:event.target.value});
      };
      updateTime1 = (event) => {
        this.setState({time1Input:event.target.value});
      }; 
      updateTime2 = (event) => {
        this.setState({time2Input:event.target.value});
      }; 
      updateMinLength = (event) => {
        this.setState({minLengthInput:event.target.value});
      }; 
      updateMaxLength = (event) => {
        this.setState({maxLengthInput:event.target.value});
      }; 
    
      handleSubmit = (event) =>{
        event.preventDefault();
        //let dataList  = [ 3, this.state.nameInput, this.state.time1Input, this.state.time2Input, this.state.minLengthInput, this.state.maxLengthInput];
        let data = {
          name: this.state.nameInput,
          type: "da",
          start: this.state.time1Input, 
          end: this.state.time2Input, 
          min_hours: this.state.minLengthInput,
          max_hours: this.state.maxLengthInput
      
        };
        axios.post('http://localhost:5001/api/schedulers/myActivities', data)
          .then(response => {
            console.log(response.data); // Handle success, e.g., show a success message
          })
          .catch(error => {
            console.error('Error saving data:', error); // Handle error, e.g., show an error message
          });
      };

    // Handle change event when a radio button is selected
    //state is managed within the component itself
    
    render() {

      return (
        <div>
        <div>Please enter the info for creating your Daily Activity</div>
        <br/>
        <form onSubmit={this.handleSubmit}>
          Name&nbsp;
          <input
            type="text"
            id="title"
            value={this.state.nameInput}
            onChange={this.updateName}
          />
          <br/>
          Window start time&nbsp;
          <input
            type="time"
            id="time1"
            value={this.state.time1Input}
            onChange={this.updateTime1}
          />
          <br/>
          Window end time&nbsp;
          <input
            type="time"
            id="time2"
            value={this.state.time2Input}
            onChange={this.updateTime2}
          />
          <br/>
          Min Length&nbsp;
          <input
            type="number"
            id="minLength"
            value={this.state.minLengthInput}
            onChange={this.updateMinLength}
          />
          <br/>
          Max Length&nbsp;
          <input
            type="number"
            id="maxLength"
            value={this.state.maxLengthInput}
            onChange={this.updateMaxLength}
          />

          <br/>
          <br/>
          <button type="submit">Submit</button>
        </form>
      </div>

      );
    }

}

class DeadlineForm extends Component{
  constructor(props) {
      super(props);
      this.state = {
        nameInput: props.name || '' ,// Initialize states
        dateInput: props.date || '', 
        hoursInput: props.hours_left || '',
        minLengthInput: props.min_hours || '',
        maxLengthInput: props.max_hours || ''
      };
    }

      updateName = (event) => {
        this.setState({nameInput:event.target.value});
      };
      updateDate= (event) => {
        this.setState({dateInput:event.target.value});
      };
      updateHours = (event) => {
        this.setState({hoursInput:event.target.value});
      }; 
      updateMinLength = (event) => {
        this.setState({minLengthInput:event.target.value});
      }; 
      updateMaxLength = (event) => {
        this.setState({maxLengthInput:event.target.value});
      }; 
      
      handleSubmit = (event) =>{
        event.preventDefault();
        let dataList  = [ 4, this.state.nameInput, this.state.dateInput, this.state.hoursInput, this.state.minLengthInput, this.state.maxLengthInput];
        let data = {
          name: this.state.nameInput,
          type: "de",
          date: this.state.dateInput,
          hours_left: this.state.hoursInput,
          min_hours: this.state.minLengthInput,
          max_hours: this.state.maxLengthInput
        };
        axios.post('http://localhost:5001/api/schedulers/myActivities', data)
          .then(response => {
            console.log(response.data); // Handle success, e.g., show a success message
          })
          .catch(error => {
            console.error('Error saving data:', error); // Handle error, e.g., show an error message
          });
      };

      

      //"name,deadline date(y/m/d),total required hours,minimum working period length,maximum working period length\n"            
      //"ex: comp project 2,2024-07-28,6.5,0.5,1.5\n"))

    
  
  
//     // Handle change event when a radio button is selected
//     //state is managed within the component itself
    
    render() {

      return (
        <div>
        <div>Please enter the info for creating your commitment</div>
        <br/>
        <form onSubmit={this.handleSubmit}>
          Name&nbsp;
          <input
            type="text"
            id="title"
            value={this.state.nameInput}
            onChange={this.updateName}
          />
          <br/>
          Date&nbsp;
            <input
              type="date"
              id="date"
              value={this.state.dateInput}
              onChange={this.updateDate}
            />
          <br/>
          Estimated Required Hours&nbsp;
          <input
            type="number"
            id="hours"
            value={this.state.hoursInput}
            onChange={this.updateHours}
          />
          <br/>
          Minimum period of time to work on this per session&nbsp;
          <input
            type="number"
            id="minLength"
            value={this.state.minLengthInput}
            onChange={this.updateMinLength}
          />
          <br/>
          Maximum period of time to work on this per session&nbsp;
          <input
            type="number"
            id="maxLength"
            value={this.state.maxLengthInput}
            onChange={this.updateMaxLength}
          />

          <br/>
          <br/>
          <button type="submit">Submit</button>
        </form>
      </div>

      );
    }

}

class HobbyForm extends Component{
  //"name,desired frequency,last performed date (y-m-d),minimum required hours,max hours\n"
  //"ex: painting,3,2024-07-07,1.5,4\n"))
  //
  constructor(props) {
      super(props);
      this.state = {
        nameInput: props.name || '' ,// Initialize states 
        frequencyInput: props.frequency || '',
        lastPerformed: props.date || '',
        minLengthInput: props.min_hours || '',
        maxLengthInput: props.max_hours || '', 
        time1Input: props.start || '',
        time2Input: props.end || ''
      };
    }

      updateName = (event) => {
        this.setState({nameInput:event.target.value});
      };
      updateFrequency = (event) => {
        this.setState({frequencyInput:event.target.value});
      }; 
      updateLastPerformed = (event) => {
        this.setState({lastPerformed:event.target.value});
      }; 
      updateMinLength = (event) => {
        this.setState({minLengthInput:event.target.value});
      }; 
      updateMaxLength = (event) => {
        this.setState({maxLengthInput:event.target.value});
      }; 
      updateTime1 = (event) => {
        this.setState({time1Input:event.target.value});
      }; 
      updateTime2 = (event) => {
        this.setState({time2Input:event.target.value});
      }; 
      
      handleSubmit = (event) =>{
        event.preventDefault();
        let data = {
          name: this.state.nameInput,
          type: "ho",
          frequency: this.state.frequencyInput,
          date: this.state.lastPerformed,
          min_hours: this.state.minLengthInput,
          max_hours: this.state.maxLengthInput, 
          start: this.state.time1Input, 
          end:this.state.time2Input
        };
        axios.post('http://localhost:5001/api/schedulers/myActivities', data)
          .then(response => {
            console.log(response.data); // Handle success, e.g., show a success message
          })
          .catch(error => {
            console.error('Error saving data:', error); // Handle error, e.g., show an error message
          });
      };

      


    
  
  
    // Handle change event when a radio button is selected
    //state is managed within the component itself
    
    render() {

      return (
        <div>
        <div>Please enter the info for creating your Hobby</div>
        <br/>
        <form onSubmit={this.handleSubmit}>
          Name&nbsp;
          <input
            type="text"
            id="title"
            value={this.state.nameInput}
            onChange={this.updateName}
          />
          <br/>
          Desired Frequency&nbsp;
          <input
            type="number"
            id="time1"
            value={this.state.frequencyInput}
            onChange={this.updateFrequency}
          />
          <br/>
          Date Last Performed&nbsp;
          <input
            type="date"
            id="date"
            value={this.state.lastPerformed}
            onChange={this.updateLastPerformed}
          />
          <br/>
          Minimum period of time to work on this per session&nbsp;
          <input
            type="number"
            id="minLength"
            value={this.state.minLengthInput}
            onChange={this.updateMinLength}
          />
          <br/>
          Maximum period of time to work on this per session&nbsp;
          <input
            type="number"
            id="maxLength"
            value={this.state.maxLengthInput}
            onChange={this.updateMaxLength}
          />
          <br/>
          Window start time&nbsp;
          <input
            type="time"
            id="time1"
            value={this.state.time1Input}
            onChange={this.updateTime1}
          />
          <br/>
          Window end time&nbsp;
          <input
            type="time"
            id="time2"
            value={this.state.time2Input}
            onChange={this.updateTime2}
          />

          <br/>
          <br/>
          <button type="submit">Submit</button>
        </form>
      </div>

      );
    }

}



export { RecurringForm, CommitmentForm, DailyForm, DeadlineForm, HobbyForm };
