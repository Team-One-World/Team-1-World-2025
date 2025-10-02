import { useState, useEffect, useCallback } from "react";
import api from "../api";
import Papa from 'papaparse';
import VisualizationShell from '../components/VisualizationShell';
import ChartsPanel from '../components/ChartsPanel';
import LoadingSpinner from "../components/LoadingSpinner";

function Home({ planets, setPlanets }) {
    const [predictionResults, setPredictionResults] = useState([]);
    const [csvData, setCsvData] = useState([]);
    const [stars, setStars] = useState([]);
    const [loading, setLoading] = useState(false);
    const [isVisualizationFullscreen, setIsVisualizationFullscreen] = useState(false);
    const [formData, setFormData] = useState({
        name: '',
        star_name: '',
        orbital_period: '',
        radius: '',
        ra: '',
        dec: '',
        duration: '',
        transit_depth: '',
        star_temp: '',
        star_radius: '',
        model_snr: ''
    });

    useEffect(() => {
        getStars();
        getPlanets();
    }, []);

    const getPlanets = () => {
        api.get('/api/planets/')
            .then(res => setPlanets(res.data))
            .catch(err => console.error(err));
    };

    const getStars = () => {
        api.get('/api/stars/')
            .then(res => setStars(res.data))
            .catch(err => console.error(err));
    };

    const fetchPlanetsForStar = useCallback(async (starData) => {
        if (!starData || !starData.id) {
            console.error("Invalid star data provided to fetchPlanetsForStar");
            return [];
        }
        try {
            const res = await api.get(`/api/stars/${starData.id}/planets/`);
            setPlanets(prev => {
                const existingPlanetIds = new Set(prev.map(p => p.id));
                const newPlanets = res.data.filter(p => !existingPlanetIds.has(p.id));
                return [...prev, ...newPlanets];
            });
            return res.data;
        } catch (err) {
            console.error(err);
            return [];
        }
    }, [setPlanets]);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({
            ...formData,
            [name]: value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            const res = await api.post('/api/predict/', formData);
            setPredictionResults([res.data]);
            setPlanets(prev => [...prev, res.data]);
            getStars(); // Refresh stars after prediction
        } catch (error) {
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            const headerMapping = {
                'display_name': 'name',
                'star_name': 'star_name',
                'period': 'orbital_period',
                'planet_radius': 'radius',
                'ra': 'ra',
                'dec': 'dec',
                'duration': 'duration',
                'transit_depth': 'transit_depth',
                'star_temp': 'star_temp',
                'star_radius': 'star_radius',
                'model_snr': 'model_snr',
                'pl_orbsmax': 'semi_major_axis',
                'koi_sma': 'semi_major_axis'
            };

            Papa.parse(file, {
                header: true,
                skipEmptyLines: true,
                transformHeader: header => {
                    const trimmedHeader = header.trim().toLowerCase();
                    return headerMapping[trimmedHeader] || trimmedHeader;
                },
                complete: (results) => {
                    setCsvData(results.data);
                },
            });
        }
    };

    const handleCsvSubmit = async () => {
        setLoading(true);
        const predictions = [];
        for (const row of csvData) {
            try {
                const res = await api.post('/api/predict/', row);
                predictions.push(res.data);
            } catch (error) {
                console.error('Error submitting row:', row, error);
            }
        }
        setPredictionResults(predictions);
        setPlanets(prev => [...prev, ...predictions]);
        getStars(); // Refresh stars after CSV submission
        setLoading(false);
    };

    const enterVisualization = () => {
        setIsVisualizationFullscreen(true);
        const el = document.documentElement;
        if (el.requestFullscreen) el.requestFullscreen().catch(()=>{});
    };

    const exitVisualization = () => {
        setIsVisualizationFullscreen(false);
        if (document.exitFullscreen) document.exitFullscreen().catch(()=>{});
    };

    if (isVisualizationFullscreen) {
        return (
            <VisualizationShell 
                stars={stars} 
                fetchPlanetsForStar={fetchPlanetsForStar} 
                isFullscreen={isVisualizationFullscreen} 
                onEnter={enterVisualization} 
                onExit={exitVisualization} 
            />
        )
    }

    return (
        <div className="min-h-screen p-4 sm:p-6 lg:p-8 fade-in">
            <header className="text-center mb-10">
                <h1 className="text-4xl sm:text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-indigo-600">
                    Exo-Planet Predictive Analysis
                </h1>
                <p className="text-gray-400 mt-2">Explore, Predict, and Visualize the Cosmos</p>
            </header>
            
            <main className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Left Column: Prediction Forms & Results */}
                <div className="lg:col-span-1 space-y-8">
                    <div className="glass-panel p-6 fade-in">
                        <h2 className="text-2xl font-bold mb-4">Predict Planet Classification</h2>
                        <form onSubmit={handleSubmit} className="space-y-4">
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <input type="text" name="name" placeholder="Planet Name" value={formData.name} onChange={handleChange} className="input-field" />
                                <input type="text" name="star_name" placeholder="Star Name" value={formData.star_name} onChange={handleChange} required className="input-field" />
                                <input type="number" name="orbital_period" placeholder="Orbital Period" value={formData.orbital_period} onChange={handleChange} required className="input-field" />
                                <input type="number" name="radius" placeholder="Radius" value={formData.radius} onChange={handleChange} required className="input-field" />
                                <input type="number" name="ra" placeholder="RA" value={formData.ra} onChange={handleChange} required className="input-field" />
                                <input type="number" name="dec" placeholder="Dec" value={formData.dec} onChange={handleChange} required className="input-field" />
                                <input type="number" name="duration" placeholder="Duration" value={formData.duration} onChange={handleChange} required className="input-field" />
                                <input type="number" name="transit_depth" placeholder="Transit Depth" value={formData.transit_depth} onChange={handleChange} required className="input-field" />
                                <input type="number" name="star_temp" placeholder="Star Temp" value={formData.star_temp} onChange={handleChange} required className="input-field" />
                                <input type="number" name="star_radius" placeholder="Star Radius" value={formData.star_radius} onChange={handleChange} required className="input-field" />
                                <input type="number" name="model_snr" placeholder="Model SNR" value={formData.model_snr} onChange={handleChange} required className="input-field" />
                            </div>
                            <button type="submit" className="btn-primary" disabled={loading}>
                                {loading ? <LoadingSpinner size={24} /> : 'Predict'}
                            </button>
                        </form>
                    </div>

                    <div className="glass-panel p-6 fade-in" style={{animationDelay: '0.1s'}}>
                        <h3 className="text-xl font-bold mb-4">Or Upload a CSV</h3>
                        <input type="file" accept=".csv" onChange={handleFileChange} className="block w-full text-sm text-gray-400 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100" />
                        <button onClick={handleCsvSubmit} disabled={csvData.length === 0 || loading} className="mt-4 btn-primary disabled:bg-gray-500 disabled:transform-none">
                            {loading ? <LoadingSpinner size={24} /> : 'Submit CSV'}
                        </button>
                    </div>

                    {predictionResults.length > 0 && (
                        <div className="glass-panel p-6 fade-in" style={{animationDelay: '0.2s'}}>
                            <h3 className="text-xl font-bold mb-4">Prediction Results</h3>
                            <ul className="space-y-3">
                                {predictionResults.map((result, index) => (
                                    <li key={index} className="bg-gray-700 bg-opacity-50 p-3 rounded-md">
                                        <p><strong>Name:</strong> {result.name}</p>
                                        <p><strong>Classification:</strong> <span className="font-semibold text-purple-300">{result.classification}</span></p>
                                        <p><strong>Confidence:</strong> <span className="font-semibold text-green-300">{(result.confidence * 100).toFixed(2)}%</span></p>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    )}
                </div>

                {/* Right Column: Visualization & Charts */}
                <div className="lg:col-span-2 space-y-8">
                    <div className="glass-panel p-6 fade-in" style={{animationDelay: '0.3s'}}>
                        <h2 className="text-2xl font-bold mb-4 text-center">Interactive Galaxy</h2>
                        <VisualizationShell stars={stars} fetchPlanetsForStar={fetchPlanetsForStar} isFullscreen={isVisualizationFullscreen} onEnter={enterVisualization} onExit={exitVisualization} />
                    </div>
                    <div className="glass-panel p-6 fade-in" style={{animationDelay: '0.4s'}}>
                        <h2 className="text-2xl font-bold mb-4 text-center">Stellar Analytics</h2>
                        <ChartsPanel sampleStars={stars} />
                    </div>
                </div>
            </main>
        </div>
    );
}

export default Home;
