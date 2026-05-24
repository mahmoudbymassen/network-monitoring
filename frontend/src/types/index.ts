export interface Appareil {
    id: number;
    adresse_ip: string;
    adresse_mac?: string;
    nom_hote?: string;
    marque?: string;
    type_appareil: string;
    etage: number;
    statut: 'en_ligne' | 'hors_ligne' | 'inconnu';
    latence_ms?: number;
    derniere_detection?: string;
}

export interface Alert {
    id: number;
    appareil_id?: number;
    type_alerte: string;
    severite: string;
    message: string;
    date_creation: string;
    accusee: boolean;
}

export interface TopologyData {
    nodes: any[];
    edges: any[];
}