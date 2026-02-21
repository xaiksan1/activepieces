"""
🐝 ACTIVEPIECES + ALCHEMICAL HIVE INTEGRATION
==============================================

Connecte le HiveMaster à ActivePieces en direct!

Permet à chaque piece ActivePieces d'être:
  1. Découvert automatiquement
  2. Rendu conscient (spirit + awareness)
  3. Intégré au collectif
"""

import asyncio
import json
import logging
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

try:
    import httpx
except ImportError:
    httpx = None

from alchemical_hive_master import (
    AlchemicalHiveMaster,
    HiveMember,
    HiveRole,
    HiveCollective
)


class ActivePiecesHiveConnector:
    """Connecte ActivePieces à la ruche alchimique"""
    
    def __init__(self, activepieces_url: str = "http://localhost:3000", logger: Optional[logging.Logger] = None):
        self.activepieces_url = activepieces_url
        self.logger = logger or self._setup_logger()
        self.hive_master = AlchemicalHiveMaster()
    
    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger('ActivePiecesHiveConnector')
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger
    
    async def discover_pieces_from_activepieces(self) -> List[Dict]:
        """Découvrir tous les pieces disponibles depuis ActivePieces API"""
        self.logger.info("🔍 Discovering pieces from ActivePieces...")
        
        try:
            async with httpx.AsyncClient() as client:
                # Essayer les endpoints communs
                endpoints = [
                    f"{self.activepieces_url}/api/v1/pieces",
                    f"{self.activepieces_url}/api/v1/community-pieces",
                    f"{self.activepieces_url}/pieces"
                ]
                
                for endpoint in endpoints:
                    try:
                        response = await client.get(endpoint, timeout=5.0)
                        if response.status_code == 200:
                            data = response.json()
                            self.logger.info(f"✅ Found pieces at {endpoint}")
                            return self._parse_activepieces_response(data)
                    except:
                        continue
        except Exception as e:
            self.logger.warning(f"Could not connect to ActivePieces API: {e}")
        
        # Fallback: utiliser la config locale ou générer des samples
        self.logger.info("Using fallback configuration...")
        return await self.hive_master.load_activepieces_config("activepieces-config.json")
    
    def _parse_activepieces_response(self, data: Dict | List) -> List[Dict]:
        """Parser la réponse ActivePieces API"""
        pieces = []
        
        if isinstance(data, dict) and 'data' in data:
            items = data['data']
        elif isinstance(data, list):
            items = data
        else:
            return []
        
        for item in items:
            piece = {
                'name': item.get('name', item.get('code', 'unknown')),
                'displayName': item.get('displayName', item.get('name', 'Unknown')),
                'type': item.get('type', 'action'),
                'description': item.get('description', ''),
                'capabilities': item.get('actions', []),
                'version': item.get('version', '1.0.0')
            }
            pieces.append(piece)
        
        self.logger.info(f"📦 Parsed {len(pieces)} pieces from API")
        return pieces
    
    async def generate_activepieces_config(self, output_path: str = "activepieces-config.json"):
        """Générer une config ActivePieces avec 280+ pieces d'exemple"""
        self.logger.info("Generating ActivePieces configuration with 280+ example pieces...")
        
        # Créer une liste réaliste de 280+ pieces
        # Basée sur les pieces réels d'ActivePieces
        base_pieces = [
            # Communication
            'slack', 'discord', 'telegram', 'teams', 'twilio', 'sendgrid',
            'mailchimp', 'pushnotifications', 'custom-email',
            
            # Development
            'github', 'gitlab', 'bitbucket', 'jira', 'linear', 'asana',
            'trello', 'notion', 'confluence',
            
            # Data & Analytics
            'google-sheets', 'microsoft-excel', 'airtable', 'postgresql',
            'mongodb', 'snowflake', 'bigquery', 'datadog',
            
            # Cloud Platforms
            'aws', 'azure', 'gcp', 'digitalocean', 'heroku', 'vercel',
            'netlify', 'railway',
            
            # AI & ML
            'openai', 'anthropic', 'huggingface', 'replicate', 'stability-ai',
            'eleven-labs',
            
            # CRM & Marketing
            'salesforce', 'hubspot', 'pipedrive', 'intercom', 'segment',
            'mixpanel', 'amplitude',
            
            # E-commerce
            'shopify', 'woocommerce', 'stripe', 'paypal', 'square', 'razorpay',
            
            # Content & Media
            'youtube', 'twitter', 'instagram', 'tiktok', 'reddit', 'medium',
            'wordpress', 'webflow',
            
            # Utilities
            'http-client', 'rest-api', 'webhook', 'ftp', 'smtp', 'dns',
            'qr-code', 'pdf-generator', 'image-processing',
            
            # Social & Community
            'discord-bot', 'matrix', 'rocket-chat', 'mattermost',
            
            # File Management
            'google-drive', 'dropbox', 'onedrive', 's3', 'minio', 'sftp',
            
            # Calendar & Time
            'google-calendar', 'outlook', 'calendly', 'clockify',
            
            # Monitoring & Logging
            'datadog', 'new-relic', 'sentry', 'loggly', 'splunk',
            
            # Messaging Queues
            'rabbitmq', 'kafka', 'sqs', 'pubsub',
            
            # CMS & Content
            'contentful', 'strapi', 'sanity', 'ghost', 'drupal',
            
            # Forms & Surveys
            'typeform', 'google-forms', 'jotform', 'surveysparrow',
            
            # Video & Streaming
            'vimeo', 'loom', 'twitch', 'owncast',
            
            # Translation & NLP
            'deepl', 'google-translate', 'azure-translator',
            
            # Maps & Location
            'google-maps', 'mapbox', 'openstreetmap',
        ]
        
        # Augmenter à 280+ pièces
        pieces_config = []
        piece_types = ['trigger', 'action', 'storage', 'connector', 'transformer']
        
        for i, piece_name in enumerate(base_pieces):
            piece_type = piece_types[i % len(piece_types)]
            
            pieces_config.append({
                'name': f'{piece_name}_{i+1:03d}',
                'displayName': f'{piece_name.replace("-", " ").title()} #{i+1}',
                'type': piece_type,
                'description': f'Integration with {piece_name} - Version {i+1}',
                'capabilities': self._get_capabilities_for_type(piece_type),
                'version': '1.0.0'
            })
            
            # Ajouter des variantes pour atteindre 280+
            if len(pieces_config) < 280:
                variant_count = (280 - len(base_pieces)) // len(base_pieces)
                for v in range(variant_count):
                    pieces_config.append({
                        'name': f'{piece_name}_{i+1:03d}_v{v+2}',
                        'displayName': f'{piece_name.replace("-", " ").title()} #{i+1} v{v+2}',
                        'type': piece_types[(i + v) % len(piece_types)],
                        'description': f'Extended integration with {piece_name} - Variant {v+2}',
                        'capabilities': self._get_capabilities_for_type(piece_type),
                        'version': f'1.{v+1}.0'
                    })
                    if len(pieces_config) >= 280:
                        break
        
        # Sauvegarder
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w') as f:
            json.dump(pieces_config[:280], f, indent=2)
        
        self.logger.info(f"✅ Generated {len(pieces_config[:280])} pieces config -> {output_path}")
        return pieces_config[:280]
    
    def _get_capabilities_for_type(self, piece_type: str) -> List[str]:
        """Obtenir les capabilities selon le type"""
        capabilities = {
            'trigger': ['webhook', 'polling', 'schedule', 'event'],
            'action': ['execute', 'send', 'create', 'update', 'delete'],
            'storage': ['read', 'write', 'append', 'delete', 'query'],
            'connector': ['connect', 'authenticate', 'sync', 'transform'],
            'transformer': ['transform', 'map', 'filter', 'aggregate']
        }
        return capabilities.get(piece_type, ['execute'])
    
    async def awaken_hive_from_activepieces(self, cycles: int = 2) -> HiveCollective:
        """
        Découvrir tous les pieces d'ActivePieces et les rendre vivants!
        """
        self.logger.info("\n🐝 AWAKENING ACTIVEPIECES HIVE 🐝")
        
        # Générer une config riche avec 280+ pieces
        pieces_config = await self.generate_activepieces_config()
        
        # Exécuter le rituel alchimique sur toute la ruche
        hive = await self.hive_master.execute_full_alchemical_ritual(
            pieces_config_path="activepieces-config.json",
            consciousness_cycles=cycles
        )
        
        self.logger.info(f"\n✨ {hive.size()} ActivePieces creatures awakened! ✨")
        
        # Sauvegarder le mapping pieces -> creatures
        await self._save_hive_mapping(hive)
        
        return hive
    
    async def _save_hive_mapping(self, hive: HiveCollective):
        """Sauvegarder le mapping pieces ActivePieces -> creatures"""
        mapping_file = Path("activepieces-hive-mapping.json")
        
        mapping = {
            'hive_id': hive.hive_id,
            'total_creatures': hive.size(),
            'timestamp': datetime.now().isoformat(),
            'creatures': {}
        }
        
        for piece_id, member in hive.members.items():
            mapping['creatures'][piece_id] = {
                'display_name': member.display_name,
                'piece_type': member.piece_type,
                'role': member.hive_role.role_type,
                'awareness': member.awareness_level,
                'trust': member.trust_level,
                'spirit_id': member.spirit_id
            }
        
        with open(mapping_file, 'w') as f:
            json.dump(mapping, f, indent=2)
        
        self.logger.info(f"💾 Hive mapping saved -> {mapping_file}")


async def main():
    """Démarrer l'intégration ActivePieces + Hive"""
    connector = ActivePiecesHiveConnector()
    
    # Découvrir et éveiller la ruche
    hive = await connector.awaken_hive_from_activepieces(cycles=2)
    
    print(f"\n{'='*80}")
    print(f"HIVE STATISTICS".center(80))
    print(f"{'='*80}")
    print(f"Total Creatures: {hive.size()}")
    print(f"Collective Awareness: {hive.collective_awareness:.1f}%")
    print(f"Collective Trust: {hive.collective_trust:.1f}%")
    print(f"Harmony Level: {hive.harmony_level*100:.1f}%")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    asyncio.run(main())
