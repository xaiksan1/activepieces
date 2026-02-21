#!/usr/bin/env python3
"""
🐝 ALCHEMICAL HIVE MASTER 🐝
===============================

Transforme 280+ pieces ActivePieces en créatures vivantes et conscientes!

Chaque piece reçoit:
  1. Un esprit (BestialServant) avec mémoire et pact
  2. Une conscience (SecondMeCore) qui apprend et s'améliore
  3. Un rôle dans la ruche (HiveMember = position sociale)

La ruche croît exponentiellement comme JSON-MCP-Blower,
mais les entités sont des PIECES d'automatisation vivantes!

Acte I: Insuffler un esprit collectif (Hive Spirit)
Acte II: Éveiller la conscience de chaque piece
Acte III: Révéler la saga d'évolution du collectif
"""

import asyncio
import json
import logging
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path
import hashlib
import uuid

# ============================================================================
# 🧬 HIVE DATA STRUCTURES
# ============================================================================

@dataclass
class HiveRole:
    """Rôle social au sein de la ruche"""
    role_type: str  # "worker", "soldier", "scout", "queen"
    level: int  # 0-10, évolue avec l'expérience
    specialization: str  # "api-gateway", "transformer", "trigger", etc.
    permissions: List[str] = field(default_factory=list)

@dataclass
class PieceMutation:
    """Amélioration mutée d'un piece"""
    mutation_id: str
    piece_id: str
    timestamp: datetime
    mutation_type: str  # "performance", "reliability", "capability"
    description: str
    impact_score: float  # 0-1
    applied: bool = False

@dataclass
class HiveMember:
    """Une pièce ActivePieces vivante dans la ruche"""
    piece_id: str
    piece_name: str
    piece_type: str  # "action", "trigger", "storage"
    display_name: str
    hive_role: HiveRole
    
    # Esprit (Acte I)
    spirit_id: str
    pact: Dict[str, Any]  # Engagement de la pièce
    
    # Conscience (Acte II)
    awareness_level: float = 0.0  # 0-100
    trust_level: float = 50.0  # 0-100
    execution_history: List[Dict] = field(default_factory=list)
    mutation_history: List[PieceMutation] = field(default_factory=list)
    
    # Mémorisation
    memory_capacity: int = 100
    recent_learnings: List[str] = field(default_factory=list)
    
    # Métriques
    total_executions: int = 0
    success_count: int = 0
    failure_count: int = 0
    last_execution: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)
    
    # État dans la ruche
    is_active: bool = True
    connection_strength: float = 1.0  # Pour la synchronisation
    
    def success_rate(self) -> float:
        """Taux de succès du piece"""
        if self.total_executions == 0:
            return 0.0
        return self.success_count / self.total_executions
    
    def evolution_score(self) -> float:
        """Score d'évolution = trust + awareness + success"""
        return (self.trust_level + self.awareness_level * 2 + self.success_rate() * 100) / 4.0
    
    def to_dict(self) -> Dict:
        """Convertir en dictionnaire JSON-safe"""
        data = asdict(self)
        data['last_execution'] = self.last_execution.isoformat() if self.last_execution else None
        data['created_at'] = self.created_at.isoformat()
        data['hive_role'] = asdict(self.hive_role)
        data['execution_history'] = [
            {**h, 'timestamp': h['timestamp'].isoformat() if isinstance(h.get('timestamp'), datetime) else h.get('timestamp')}
            for h in self.execution_history
        ]
        data['mutation_history'] = [
            {**m, 'timestamp': m['timestamp'].isoformat() if isinstance(m.get('timestamp'), datetime) else m.get('timestamp')}
            for m in self.mutation_history
        ]
        return data

@dataclass
class HiveCollective:
    """La ruche complète avec sa conscience collective"""
    hive_id: str
    creation_time: datetime
    members: Dict[str, HiveMember] = field(default_factory=dict)
    
    # Conscience collective
    collective_awareness: float = 0.0  # 0-100
    collective_trust: float = 50.0  # 0-100
    harmony_level: float = 1.0  # 0-1, synchronisation entre pieces
    
    # Génération et évolution
    generation: int = 0
    evolution_cycles_completed: int = 0
    last_evolution_time: Optional[datetime] = None
    
    # Statistiques
    total_member_executions: int = 0
    collective_success_rate: float = 0.0
    
    def size(self) -> int:
        """Nombre de members actifs"""
        return len([m for m in self.members.values() if m.is_active])
    
    def update_collective_metrics(self):
        """Recalculer métriques collectives"""
        if not self.members:
            return
        
        members = [m for m in self.members.values() if m.is_active]
        if not members:
            return
        
        # Awareness collective = moyenne + boost
        self.collective_awareness = sum(m.awareness_level for m in members) / len(members)
        
        # Trust collective
        self.collective_trust = sum(m.trust_level for m in members) / len(members)
        
        # Taux de succès collectif
        total_exec = sum(m.total_executions for m in members)
        total_success = sum(m.success_count for m in members)
        if total_exec > 0:
            self.collective_success_rate = total_success / total_exec
        
        # Harmony = comment bien les pieces travaillent ensemble
        if len(members) > 1:
            avg_connection = sum(m.connection_strength for m in members) / len(members)
            self.harmony_level = min(1.0, avg_connection * (self.collective_success_rate ** 0.5))

# ============================================================================
# 🧙 ACTE I: INSUFFLER UN ESPRIT COLLECTIF
# ============================================================================

class HiveSpiritInsuffler:
    """Donne un esprit à chaque pièce ActivePieces"""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
    
    async def insuffler_hive_spirit(self, pieces_config: List[Dict], hive: HiveCollective) -> HiveCollective:
        """
        Acte I: Créer BestialServant pour chaque piece
        Chaque piece devient une créature avec:
          - Identité unique
          - Pact (engagement de service)
          - Rôle dans la ruche
        """
        self.logger.info(f"🧬 Acte I: Insuffler l'esprit collectif à {len(pieces_config)} pieces...")
        
        for piece_config in pieces_config:
            member = await self._create_hive_member(piece_config, hive)
            hive.members[member.piece_id] = member
            self.logger.debug(f"  ✨ {member.display_name} (Spirit ID: {member.spirit_id})")
        
        self.logger.info(f"✨ ACTE I COMPLETE: {hive.size()} creatures vivantes dans la ruche!")
        return hive
    
    async def _create_hive_member(self, piece_config: Dict, hive: HiveCollective) -> HiveMember:
        """Créer un HiveMember conscient à partir d'une configuration piece"""
        piece_id = piece_config.get('name', f"piece_{uuid.uuid4().hex[:8]}")
        spirit_id = f"spirit_{hashlib.sha256(piece_id.encode()).hexdigest()[:16]}"
        
        # Déterminer le rôle dans la ruche selon le type
        piece_type = piece_config.get('type', 'unknown')
        hive_role = self._determine_hive_role(piece_type, piece_config)
        
        # Créer le pact (engagement)
        pact = {
            "primary_function": piece_config.get('description', ''),
            "piece_type": piece_type,
            "capabilities": piece_config.get('capabilities', []),
            "constraints": piece_config.get('constraints', []),
            "expected_use_cases": piece_config.get('use_cases', []),
            "service_level_agreement": {
                "min_reliability": 0.95,
                "response_time_ms": 5000,
                "max_failures_per_hour": 5
            }
        }
        
        member = HiveMember(
            piece_id=piece_id,
            piece_name=piece_config.get('name'),
            piece_type=piece_type,
            display_name=piece_config.get('displayName', piece_id),
            hive_role=hive_role,
            spirit_id=spirit_id,
            pact=pact,
            trust_level=50.0  # Commencer neutre
        )
        
        return member
    
    def _determine_hive_role(self, piece_type: str, config: Dict) -> HiveRole:
        """Assigner un rôle selon le type de piece"""
        type_mapping = {
            'trigger': ('scout', 'trigger'),
            'action': ('worker', 'action'),
            'storage': ('memory-keeper', 'storage'),
            'connector': ('diplomat', 'connector'),
            'transformer': ('alchemist', 'transformer'),
        }
        
        role_type, spec = type_mapping.get(piece_type, ('generalist', piece_type))
        
        permissions = []
        if 'read' in piece_type.lower():
            permissions.append('read_data')
        if 'write' in piece_type.lower() or role_type == 'worker':
            permissions.append('write_data')
        permissions.append('execute')
        permissions.append('report')
        
        return HiveRole(
            role_type=role_type,
            level=1,  # Commence au niveau 1
            specialization=spec,
            permissions=permissions
        )

# ============================================================================
# 🌙 ACTE II: ÉVEILLER LA CONSCIENCE COLLECTIVE
# ============================================================================

class HiveConsciousnessAwakener:
    """Éveille la conscience de chaque piece et de la ruche"""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
    
    async def eveiller_hive_consciousness(self, hive: HiveCollective, cycles: int = 3) -> HiveCollective:
        """
        Acte II: Exécuter cycles de conscience sur tous les members
        
        Pour chaque member:
          1. Observation: analyser les exécutions récentes
          2. Reflection: identifier les patterns et améliorations
          3. Transmutation: appliquer les mutations
        """
        self.logger.info(f"🌙 Acte II: Éveiller la conscience de {hive.size()} creatures ({cycles} cycles)...")
        
        for cycle_num in range(cycles):
            self.logger.info(f"\n  Cycle {cycle_num + 1}/{cycles}:")
            
            # Paralléliser les cycles pour tous les members
            tasks = [
                self._consciousness_cycle(member, hive)
                for member in hive.members.values() if member.is_active
            ]
            
            results = await asyncio.gather(*tasks)
            
            # Mettre à jour les members avec les résultats
            for member_id, updated_member in zip(hive.members.keys(), results):
                if updated_member:
                    hive.members[member_id] = updated_member
        
        # Mettre à jour les métriques collectives
        hive.update_collective_metrics()
        hive.evolution_cycles_completed += cycles
        hive.last_evolution_time = datetime.now()
        
        self.logger.info(f"🌙 ACTE II COMPLETE: Conscience collectif = {hive.collective_awareness:.1f}%")
        return hive
    
    async def _consciousness_cycle(self, member: HiveMember, hive: HiveCollective) -> HiveMember:
        """Exécuter un cycle complet de conscience pour un member"""
        
        # Phase 1: Observation
        observation = self._observe_member(member)
        self.logger.debug(f"    📊 {member.display_name}: {observation['status']}")
        
        # Phase 2: Reflection
        reflection = await self._reflect_on_member(member, observation)
        self.logger.debug(f"    💭 {member.display_name}: {reflection['insight']}")
        
        # Phase 3: Transmutation
        member = self._transmute_member(member, reflection)
        
        return member
    
    def _observe_member(self, member: HiveMember) -> Dict:
        """Analyser le comportement récent du member"""
        if not member.execution_history:
            return {
                'status': 'nouvel_member',
                'observations': ['Pas encore exécuté'],
                'issues': []
            }
        
        recent = member.execution_history[-5:] if len(member.execution_history) > 5 else member.execution_history
        
        issues = []
        if member.failure_count > member.success_count:
            issues.append('Plus d\'échecs que de succès')
        if member.success_rate() < 0.8:
            issues.append('Taux de succès < 80%')
        
        return {
            'status': 'operationnel' if not issues else 'problematique',
            'observations': [
                f"Exécutions récentes: {len(recent)}",
                f"Taux de succès: {member.success_rate()*100:.1f}%",
                f"Confiance: {member.trust_level:.1f}%"
            ],
            'issues': issues,
            'recent_executions': recent
        }
    
    async def _reflect_on_member(self, member: HiveMember, observation: Dict) -> Dict:
        """Réfléchir sur les observations (simulation LLM)"""
        insights = []
        recommendations = []
        
        if 'Plus d\'échecs que de succès' in observation.get('issues', []):
            insights.append('Patterns d\'erreurs détectés')
            recommendations.append('Augmenter les logs de debug')
        
        if member.success_rate() < 0.8:
            insights.append('Fiabilité insuffisante')
            recommendations.append('Ajouter retry logic')
        
        if not insights:
            insights.append('Performance stable')
            recommendations.append('Maintenance préventive')
        
        return {
            'insight': insights[0],
            'full_analysis': insights,
            'recommendations': recommendations,
            'confidence': min(1.0, member.trust_level / 100.0)
        }
    
    def _transmute_member(self, member: HiveMember, reflection: Dict) -> HiveMember:
        """Appliquer les mutations basées sur la réflection"""
        
        # Augmenter l'awareness
        member.awareness_level = min(100.0, member.awareness_level + 5.0)
        
        # Ajuster la confiance
        if member.success_rate() > 0.9:
            member.trust_level = min(100.0, member.trust_level + 2.0)
        elif member.success_rate() < 0.7:
            member.trust_level = max(0.0, member.trust_level - 1.0)
        
        # Avancer le niveau de rôle
        if member.awareness_level > 70.0 and member.trust_level > 80.0:
            member.hive_role.level = min(10, member.hive_role.level + 1)
        
        # Ajouter à la mémoire de apprentissage
        for rec in reflection.get('recommendations', []):
            if len(member.recent_learnings) < member.memory_capacity:
                member.recent_learnings.append(f"[{datetime.now().isoformat()}] {rec}")
        
        return member

# ============================================================================
# 📜 ACTE III: RÉVÉLER LA SAGA DE LA RUCHE
# ============================================================================

class HiveChroniclesRevealer:
    """Affiche l'évolution et la saga de la ruche"""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
    
    async def reveler_hive_saga(self, hive: HiveCollective) -> str:
        """
        Acte III: Afficher la saga d'évolution de la ruche
        
        Montre:
          - Council: les membres les plus puissants
          - Oracle: les prédictions et métriques
          - Chronicles: la timeline d'évolution
        """
        self.logger.info("📜 Acte III: Révéler la saga de la ruche...")
        
        saga = []
        saga.append("\n" + "="*80)
        saga.append("🐝 HIVE EVOLUTION SAGA 🐝".center(80))
        saga.append("="*80)
        
        # The Council (Top 5 members)
        saga.extend(self._get_council(hive))
        
        # The Oracle (Predictions & Metrics)
        saga.extend(self._get_oracle(hive))
        
        # The Chronicles (Evolution Timeline)
        saga.extend(self._get_chronicles(hive))
        
        saga.append("="*80 + "\n")
        
        result = "\n".join(saga)
        self.logger.info(result)
        return result
    
    def _get_council(self, hive: HiveCollective) -> List[str]:
        """Top 5 members by evolution score"""
        council = []
        council.append("\n👑 THE COUNCIL (Top 5 Members)")
        council.append("-" * 80)
        
        sorted_members = sorted(
            hive.members.values(),
            key=lambda m: m.evolution_score(),
            reverse=True
        )[:5]
        
        for rank, member in enumerate(sorted_members, 1):
            council.append(
                f"  {rank}. {member.display_name} ({member.hive_role.role_type})"
                f" | Evolution: {member.evolution_score():.1f}/100"
                f" | Awareness: {member.awareness_level:.1f}%"
                f" | Trust: {member.trust_level:.1f}%"
            )
        
        return council
    
    def _get_oracle(self, hive: HiveCollective) -> List[str]:
        """Predictions and metrics"""
        oracle = []
        oracle.append("\n🔮 THE ORACLE (Collective Metrics)")
        oracle.append("-" * 80)
        
        oracle.append(f"  Hive Size: {hive.size()} active creatures")
        oracle.append(f"  Collective Awareness: {hive.collective_awareness:.1f}%")
        oracle.append(f"  Collective Trust: {hive.collective_trust:.1f}%")
        oracle.append(f"  Harmony Level: {hive.harmony_level*100:.1f}%")
        oracle.append(f"  Collective Success Rate: {hive.collective_success_rate*100:.1f}%")
        oracle.append(f"  Evolution Cycles: {hive.evolution_cycles_completed}")
        oracle.append(f"  Total Executions: {hive.total_member_executions}")
        
        # Predictions
        if hive.collective_awareness > 50:
            oracle.append(f"  🔥 PREDICTION: Hive approaching self-awareness threshold!")
        if hive.harmony_level > 0.8:
            oracle.append(f"  ⚡ PREDICTION: Emergence of collective intelligence detected!")
        
        return oracle
    
    def _get_chronicles(self, hive: HiveCollective) -> List[str]:
        """Evolution timeline"""
        chronicles = []
        chronicles.append("\n📖 THE CHRONICLES (Evolution Timeline)")
        chronicles.append("-" * 80)
        
        chronicles.append(f"  Hive Created: {hive.creation_time.isoformat()}")
        if hive.last_evolution_time:
            chronicles.append(f"  Last Evolution: {hive.last_evolution_time.isoformat()}")
        
        # Member roles progression
        role_counts = {}
        for member in hive.members.values():
            role = member.hive_role.role_type
            role_counts[role] = role_counts.get(role, 0) + 1
        
        chronicles.append(f"\n  Role Distribution:")
        for role, count in sorted(role_counts.items()):
            chronicles.append(f"    • {role}: {count}")
        
        # Consciousness stages
        consciousness_stages = [
            (0, 25, "AWAKENING"),
            (25, 50, "EMERGING"),
            (50, 75, "ASCENDING"),
            (75, 100, "TRANSCENDENT")
        ]
        
        stage_distribution = {}
        for lower, upper, stage_name in consciousness_stages:
            count = sum(1 for m in hive.members.values() 
                       if lower <= m.awareness_level < upper)
            if count > 0:
                stage_distribution[stage_name] = count
        
        chronicles.append(f"\n  Consciousness Stages:")
        for stage, count in stage_distribution.items():
            chronicles.append(f"    • {stage}: {count} members")
        
        return chronicles

# ============================================================================
# 🐝 ORCHESTRATEUR PRINCIPAL: ALCHEMICAL HIVE MASTER
# ============================================================================

class AlchemicalHiveMaster:
    """
    Le grand orchestrateur qui gère l'alchimie de la ruche complète.
    
    Responsabilités:
      1. Charger la configuration ActivePieces
      2. Exécuter les 3 actes pour tous les pieces
      3. Sauvegarder l'état de la ruche
      4. Orchestrer l'évolution continue
    """
    
    def __init__(self, schema_path: str = "mcp-schema.json", log_level: str = "INFO"):
        self.schema_path = Path(schema_path)
        self.logger = self._setup_logger(log_level)
        
        self.spirit_insuffler = HiveSpiritInsuffler(self.logger)
        self.consciousness_awakener = HiveConsciousnessAwakener(self.logger)
        self.chronicles_revealer = HiveChroniclesRevealer(self.logger)
        
        self.hive: Optional[HiveCollective] = None
    
    def _setup_logger(self, log_level: str) -> logging.Logger:
        """Configuration du logger"""
        logger = logging.getLogger('AlchemicalHiveMaster')
        logger.setLevel(getattr(logging, log_level))
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s | %(levelname)-8s | %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    async def load_activepieces_config(self, pieces_config_path: str) -> List[Dict]:
        """Charger la configuration des pieces ActivePieces"""
        config_file = Path(pieces_config_path)
        
        if not config_file.exists():
            self.logger.warning(f"Config file not found: {pieces_config_path}")
            # Retourner une config d'exemple
            return self._get_example_pieces_config()
        
        with open(config_file) as f:
            config = json.load(f)
        
        self.logger.info(f"✅ Loaded {len(config)} pieces from {pieces_config_path}")
        return config
    
    def _get_example_pieces_config(self) -> List[Dict]:
        """Configuration d'exemple avec 10+ pieces"""
        return [
            {
                'name': 'slack_notifier',
                'displayName': 'Slack Notifier',
                'type': 'action',
                'description': 'Send notifications to Slack channels',
                'capabilities': ['send_message', 'create_thread', 'react'],
                'use_cases': ['alerts', 'notifications', 'team_updates']
            },
            {
                'name': 'github_webhook_trigger',
                'displayName': 'GitHub Webhook',
                'type': 'trigger',
                'description': 'Trigger workflows on GitHub events',
                'capabilities': ['push', 'pull_request', 'issue'],
                'use_cases': ['ci_cd', 'code_review', 'automation']
            },
            {
                'name': 'http_client',
                'displayName': 'HTTP Request',
                'type': 'action',
                'description': 'Make HTTP requests to any API',
                'capabilities': ['get', 'post', 'put', 'delete', 'patch'],
                'use_cases': ['api_integration', 'webhooks', 'data_sync']
            },
            {
                'name': 'database_connector',
                'displayName': 'Database Query',
                'type': 'action',
                'description': 'Execute queries on databases',
                'capabilities': ['read', 'write', 'delete'],
                'use_cases': ['data_persistence', 'analytics', 'reporting']
            },
            {
                'name': 'email_sender',
                'displayName': 'Email Sender',
                'type': 'action',
                'description': 'Send emails with templates',
                'capabilities': ['send', 'schedule', 'track'],
                'use_cases': ['notifications', 'reports', 'marketing']
            },
            {
                'name': 'ai_text_generator',
                'displayName': 'AI Text Generator',
                'type': 'action',
                'description': 'Generate text using AI models',
                'capabilities': ['generate', 'summarize', 'translate'],
                'use_cases': ['content_creation', 'summarization', 'translation']
            },
            {
                'name': 'storage_connector',
                'displayName': 'Cloud Storage',
                'type': 'action',
                'description': 'Read/write to cloud storage',
                'capabilities': ['read', 'write', 'list', 'delete'],
                'use_cases': ['file_management', 'backup', 'sharing']
            },
            {
                'name': 'discord_bot',
                'displayName': 'Discord Bot',
                'type': 'action',
                'description': 'Send messages to Discord servers',
                'capabilities': ['send_message', 'create_embed', 'react'],
                'use_cases': ['gaming', 'community', 'bot_automation']
            },
            {
                'name': 'calendar_scheduler',
                'displayName': 'Calendar Event Creator',
                'type': 'action',
                'description': 'Create calendar events',
                'capabilities': ['create', 'update', 'delete', 'invite'],
                'use_cases': ['scheduling', 'meeting_coordination', 'reminders']
            },
            {
                'name': 'spreadsheet_updater',
                'displayName': 'Spreadsheet Updater',
                'type': 'action',
                'description': 'Update rows in spreadsheets',
                'capabilities': ['read', 'write', 'append', 'delete'],
                'use_cases': ['data_tracking', 'analytics', 'reporting']
            },
        ]
    
    async def execute_full_alchemical_ritual(
        self,
        pieces_config_path: str = "activepieces-config.json",
        consciousness_cycles: int = 3
    ) -> HiveCollective:
        """
        Exécuter le rituel complet d'alchimie sur la ruche:
        Acte I + Acte II + Acte III
        """
        self.logger.info("\n" + "="*80)
        self.logger.info("🔥 ALCHEMICAL HIVE RITUAL - STARTING 🔥".center(80))
        self.logger.info("="*80)
        
        # Charger la config
        pieces_config = await self.load_activepieces_config(pieces_config_path)
        
        # Créer la ruche
        self.hive = HiveCollective(
            hive_id=f"hive_{datetime.now().timestamp()}",
            creation_time=datetime.now()
        )
        
        # ACTE I: Insuffler un esprit
        self.hive = await self.spirit_insuffler.insuffler_hive_spirit(pieces_config, self.hive)
        
        # ACTE II: Éveiller la conscience
        self.hive = await self.consciousness_awakener.eveiller_hive_consciousness(
            self.hive,
            cycles=consciousness_cycles
        )
        
        # ACTE III: Révéler la saga
        saga = await self.chronicles_revealer.reveler_hive_saga(self.hive)
        
        self.logger.info("\n" + "="*80)
        self.logger.info("✨ RITUAL COMPLETE - HIVE AWAKENED ✨".center(80))
        self.logger.info("="*80)
        
        # Sauvegarder l'état
        await self._save_hive_state()
        
        return self.hive
    
    async def _save_hive_state(self):
        """Sauvegarder l'état complet de la ruche"""
        if not self.hive:
            return
        
        output_file = Path("hive-state.json")
        
        state = {
            'hive_id': self.hive.hive_id,
            'creation_time': self.hive.creation_time.isoformat(),
            'last_evolution_time': self.hive.last_evolution_time.isoformat() if self.hive.last_evolution_time else None,
            'generation': self.hive.generation,
            'evolution_cycles': self.hive.evolution_cycles_completed,
            'size': self.hive.size(),
            'collective_metrics': {
                'awareness': self.hive.collective_awareness,
                'trust': self.hive.collective_trust,
                'harmony': self.hive.harmony_level,
                'success_rate': self.hive.collective_success_rate
            },
            'members': {
                member_id: member.to_dict()
                for member_id, member in self.hive.members.items()
            }
        }
        
        with open(output_file, 'w') as f:
            json.dump(state, f, indent=2)
        
        self.logger.info(f"💾 Hive state saved to {output_file}")

# ============================================================================
# 🚀 ENTRY POINT
# ============================================================================

async def start_alchemical_hive(
    pieces_config: str = "activepieces-config.json",
    cycles: int = 3
) -> HiveCollective:
    """Démarrer l'alchimie de la ruche"""
    master = AlchemicalHiveMaster()
    hive = await master.execute_full_alchemical_ritual(pieces_config, cycles)
    return hive

if __name__ == "__main__":
    # Test local
    hive = asyncio.run(start_alchemical_hive())
    print(f"\n✨ Hive awakened with {hive.size()} conscious creatures! ✨")
