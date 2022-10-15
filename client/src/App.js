import "./App.css";
import React from "react";
import {
  AppBar,
  Box,
  Toolbar,
  Typography,
  Button,
  Card,
  CardActions,
  CardContent,
  Grid,
  TextField,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody
} from "@mui/material";
import { Container } from "@mui/system";

import { ThemeProvider } from "@mui/material/styles";

import AppTheme from "./AppTheme";
import env from "react-dotenv";
import axios from "axios";

const LABELS = [
  "toxic",
  "severe toxic",
  "obscene",
  "threat",
  "insult",
  "identity hate"
];
const predictionColorMapper = {
  0:"green",
  1:"red",
}

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      text: undefined,
      originalPrediction: undefined,
      processedPrediction: undefined
    };
  }

  onChange = event => {
    this.setState({ text: event.target.value });
  };

  predictText = async () => {
    if (this.state.text !== undefined && this.state.text !== "") {
      await axios
        .post(env.SERVER_URL + "/predict", { text: this.state.text })
        .then(res => {
          const processedPrediction = this.processPrediction(res.data);
          this.setState({
            originalPrediction: res.data,
            processedPrediction: processedPrediction
          });
        });
    }
  };

  processPrediction = arr => {
    return arr.map(pred => (pred > 0.5 ? 1 : 0));
  };

  getOriginalPrediction = index => {
    return (this.state.originalPrediction[index] * 100).toFixed(2);
  };

  getValueForDisplay = (text,index) => {
    return text+" (" + this.getOriginalPrediction(index) + "%)";
  }

  getProcessedPredictionsForDisplay = (pred, index) => {
    if (pred === 1) {
      return this.getValueForDisplay("yes",index);
    }
    return this.getValueForDisplay("no",index);
  };

  getProcessedPredictionsForTable = () => {
    return this.state.processedPrediction.map((pred, index) =>
      <TableCell>
        <Typography color={predictionColorMapper[pred]}>
          {this.getProcessedPredictionsForDisplay(pred, index)}
        </Typography>
      </TableCell>
    );
  };

  getLabelsForTable = () => {
    return LABELS.map(label =>
      <TableCell>
        {label}
      </TableCell>
    );
  };

  getNullValuesForTable = () => {
    return LABELS.map(label => <TableCell>N/A</TableCell>);
  };

  render() {
    return (
      <ThemeProvider theme={AppTheme}>
        <div>
          <Box sx={{ flexGrow: 1 }}>
            <AppBar position="static" color="primary">
              <Toolbar>
                <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                  Text Moderation Model Test
                </Typography>
              </Toolbar>
            </AppBar>
          </Box>
          <Container sx={{ paddingTop: 5 }}>
            <Card sx={{ maxWidth: 700 }}>
              <CardContent>
                <Typography variant="h4" gutterBottom>
                  Please enter a text
                </Typography>
                <Typography variant="h6">
                  The model will classify the text in some of these categories:
                  <br />
                </Typography>
                <Table>
                  <TableHead>
                    <TableRow>
                      {this.getLabelsForTable()}
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    <TableRow>
                      {this.state.processedPrediction
                        ? this.getProcessedPredictionsForTable()
                        : this.getNullValuesForTable()}
                    </TableRow>
                  </TableBody>
                </Table>
              </CardContent>
              <CardActions>
                <Grid container spacing={2}>
                  <Grid item xs={12}>
                    <TextField
                      id="Text"
                      label="Enter some text"
                      variant="outlined"
                      multiline
                      minRows={4}
                      sx={{ width: 500 }}
                      value={this.state.text}
                      onChange={this.onChange}
                    />
                  </Grid>
                  <Grid item>
                    <Button variant="contained" onClick={this.predictText}>
                      Get Prediction
                    </Button>
                  </Grid>
                </Grid>
              </CardActions>
            </Card>
          </Container>
        </div>
      </ThemeProvider>
    );
  }
}

export default App;
