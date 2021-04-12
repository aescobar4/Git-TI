import React from "react"
import Seasons from "./Seasons"
import EpisodeDetail from "./EpisodeDetail"
import './index.css';


class App extends React.Component {

    constructor() {
        super()
        this.state = {}
        this.handleSeriesClick = this.handleSeriesClick.bind(this)
        this.handleEpisodeClick = this.handleEpisodeClick.bind(this)
    }

    async handleSeriesClick(event, serie) {
      let aux = new Set();
      if (serie === "BCS") {
        await fetch("https://tarea-1-breaking-bad.herokuapp.com/api/episodes?series=Better+Call+Saul")
          .then(response => response.json())
          .then(data => {
            this.setState({
              episodes: data
            })
          })
      }

      if (serie === "BB") {
        await fetch("https://tarea-1-breaking-bad.herokuapp.com/api/episodes?series=Breaking+Bad")
          .then(response => response.json())
          .then(data => {
            this.setState({
              episodes: data
            })
          })
      }

      Object.keys(this.state.episodes).forEach(key => {
        let value = this.state.episodes[key];
        aux.add(value.season)
      })
      let mainList = Array.from(aux)
      mainList.sort()
      this.setState({
        seasons: mainList
      })

      let aux2 = []
      for (let season of this.state.seasons) {
        aux2.push(<Seasons key={season} season={season} episodes={this.state.episodes} episodeClick={this.handleEpisodeClick} />)
      }
      this.setState({seasonsToDeploy: aux2})
    }
    
    handleEpisodeClick(event, episode) {
      Object.keys(this.state.episodes).forEach(key => {
        let value = this.state.episodes[key];
        if (value.episode_id === episode) {
          this.setState({
            episodeToShow: <EpisodeDetail key={value.episode_id} value={value} />
          })
        }
      })
    }

    render() {
        return (
          <div className="container">
            <h1>Tarea 1 Taller de Integración</h1>
            <p>Aquí verás las series disponibles</p>
            <p>
              Cómo navegar por la página. La columna izquierda tiene series, temporadas y episodios. La barra derecha muestra
              nombre del episodio e información del personaje. Si no ves la información en la columna derecha, haz un poco de scroll, está centrado verticalmente. 
              No hay barra de búsqueda. Perdón el poco (y mal) diseño, tuve 1 día para hacer esta tarea,
              ojalá te sirva el tutorial. <br/>
            </p>
            <table>
              <tr>
                <td>
                  <button onClick={(event) => this.handleSeriesClick(event, "BB")}>Breaking Bad</button><br/>
                  <button onClick={(event) => this.handleSeriesClick(event, "BCS")}>Better Call Saul</button>
                  <div>{this.state.seasonsToDeploy}</div>
                </td>
                <td>
                  <div>{this.state.episodeToShow ? this.state.episodeToShow : "Selecciona un episodio"}</div>
                </td>
              </tr>
            </table>
          </div>
        )
    }
}

export default App