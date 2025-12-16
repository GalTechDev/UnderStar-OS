/**
 * UnderStar-OS i18n (Internationalization) System
 * Handles dynamic language switching without page reload
 * 
 * Embedded translations to avoid CORS issues with file:// protocol
 */

const i18n = {
    currentLang: 'en',
    supportedLangs: ['en', 'fr'],

    // Embedded translations (no fetch required)
    allTranslations: {
        en: {
            nav: {
                home: "Home",
                getStarted: "Get Started",
                documentation: "Documentation",
                github: "GitHub"
            },
            getStarted: {
                title: "Get Started",
                subtitle: "Before coding, understand how the framework works. You'll be more efficient and know how to debug.",
                understand: {
                    title: "🧠 Understanding the Architecture",
                    whyPlugins: {
                        title: "🤔 Why a plugin system?",
                        content: "A classic Discord bot quickly becomes a giant 2000+ line file impossible to maintain. With plugins, each feature is <strong>isolated</strong>: you can add, modify or remove a feature without touching the rest of the code."
                    },
                    lifecycle: {
                        title: "The Lifecycle",
                        content: "When you launch your bot, here's what happens behind the scenes:",
                        diagramTitle: "Startup cycle",
                        step1: { label: "OS.start()", sublabel: "Entry point" },
                        step2: { label: "Scan plugins/", sublabel: "Discovery" },
                        step3: { label: "on_load()", sublabel: "Initialization" },
                        step4: { label: "on_ready()", sublabel: "Bot connected" }
                    },
                    remember: {
                        title: "💡 Remember",
                        content: "<code>on_load()</code> is called BEFORE the Discord connection (to prepare data), <code>on_ready()</code> is called AFTER (for actions that require the Discord API)."
                    },
                    concepts: {
                        title: "Key Concepts",
                        plugin: {
                            title: "🧩 Plugin",
                            content: "A Python class that inherits from <code>Plugin</code>. It has access to the logger, data manager, and can declare commands/events."
                        },
                        eventBus: {
                            title: "⚡ Event Bus",
                            content: "Communication system between plugins. A plugin can emit an event, others can listen without direct dependency."
                        },
                        dataManager: {
                            title: "💾 Data Manager",
                            content: "Automatic JSON storage. No file management needed, the framework scopes data by guild, user, or global."
                        }
                    }
                },
                installation: {
                    title: "📦 Installation",
                    prerequisites: {
                        title: "✅ Prerequisites",
                        content: "Python 3.10+ and git installed on your machine. A Discord bot token (created on the <a href=\"https://discord.com/developers/applications\" target=\"_blank\">Developer Portal</a>)."
                    }
                },
                quickStart: {
                    title: "⚡ Quick Start",
                    createFile: "Create a file named <code>main.py</code>:",
                    whatItDoes: {
                        title: "💡 What does this code do?",
                        content: "<strong>Line 1</strong>: Imports the main class of the framework.<br><strong>Line 4</strong>: Creates an instance of your bot's \"operating system\".<br><strong>Line 5</strong>: Starts the main loop. On first launch, the token will be requested and saved automatically."
                    },
                    runBot: "Run the bot:"
                },
                structure: {
                    title: "📁 Project Structure",
                    content: "After the first launch, the framework creates this structure:",
                    warning: {
                        title: "⚠️ Important",
                        content: "The <code>data/token/</code> folder contains your Discord token. <strong>Never commit it to Git!</strong> Add <code>data/</code> to your <code>.gitignore</code>."
                    }
                },
                nextSteps: {
                    title: "🎯 Next Steps",
                    step1: {
                        title: "Create your first plugin",
                        content: "Read the <a href=\"docs.html#plugin-structure\">Plugin Structure</a> section to understand how to create a plugin."
                    },
                    step2: {
                        title: "Add a command",
                        content: "Use the <code>@slash_command</code> decorator to create Discord slash commands."
                    },
                    step3: {
                        title: "Listen to events",
                        content: "React to messages, reactions, members joining with <code>@listen</code>."
                    },
                    readDocs: "Read Full Documentation →"
                }
            },
            docs: {
                title: "Documentation",
                subtitle: "Complete API reference. Each section explains the <strong>how</strong> and the <strong>why</strong>.",
                pluginStructure: {
                    title: "🧩 Plugin Structure",
                    whatIs: {
                        title: "💡 What is a Plugin?",
                        content: "A plugin is a <strong>Python class</strong> that represents a feature of your bot. By inheriting from <code>Plugin</code>, your class automatically gets access to the logger, data manager, and can declare commands and listeners."
                    },
                    minimalStructure: "Minimal plugin structure:",
                    lifecycle: {
                        title: "Plugin Lifecycle",
                        diagramTitle: "Lifecycle methods",
                        onLoad: { label: "on_load()", sublabel: "Before connection" },
                        onReady: { label: "on_ready()", sublabel: "After connection" },
                        onUnload: { label: "on_unload()", sublabel: "Plugin stop" }
                    },
                    whySeparate: {
                        title: "🤔 Why separate on_load and on_ready?",
                        content: "<code>on_load()</code> runs BEFORE Discord connection — use it to load configs, prepare data. <code>on_ready()</code> runs AFTER — use it to get guild info, send startup messages, etc."
                    },
                    autoAccess: "What you get automatically",
                    logger: "Pre-configured logger with your plugin name",
                    data: "Data Manager for persistent data storage",
                    bot: "Discord client instance (after on_ready)"
                },
                commands: {
                    title: "⚡ Slash Commands",
                    howItWorks: {
                        title: "💡 How does it work?",
                        content: "The <code>@slash_command</code> decorator registers your function as a Discord command. At startup, the framework collects all commands and syncs them with the Discord API. When a user types <code>/your_command</code>, Discord calls your function with an <code>Interaction</code> object."
                    },
                    parameters: "Command Parameters",
                    parametersDesc: "Add parameters by declaring them in the function signature:",
                    timeout: {
                        title: "⚠️ 3 second timeout",
                        content: "Discord expects a response within <strong>3 seconds</strong>. If your processing is long, use <code>interaction.response.defer()</code> then <code>interaction.followup.send()</code>."
                    }
                },
                events: {
                    title: "👂 Event Listener",
                    eventBus: {
                        title: "💡 The Event Bus",
                        content: "Discord sends \"events\" when something happens (message received, member joins, reaction added...). The <code>@listen</code> decorator tells the framework: \"when this event arrives, call my function\"."
                    },
                    availableEvents: "Available Events",
                    onMessage: "A message is sent",
                    onMemberJoin: "A member joins a server",
                    onReactionAdd: "A reaction is added",
                    onVoiceState: "Someone joins/leaves a voice channel",
                    bestPractice: {
                        title: "✅ Best Practice",
                        content: "Always check <code>message.author.bot</code> in <code>ON_MESSAGE</code> to avoid your bot responding to itself in an infinite loop!"
                    }
                },
                tasks: {
                    title: "⏰ Scheduled Tasks",
                    background: {
                        title: "💡 Background Tasks",
                        content: "Sometimes you want to run code at regular intervals (check an API, send a reminder...). The <code>@task</code> decorator creates a loop that runs automatically."
                    },
                    timingOptions: "Timing Options",
                    seconds: "Every 30 seconds",
                    minutes: "Every 5 minutes",
                    hours: "Every hour",
                    errorHandling: {
                        title: "⚠️ Error Handling",
                        content: "If your task crashes, it stops! Wrap your code in a <code>try/except</code> to prevent an error from completely stopping the task."
                    }
                },
                data: {
                    title: "💾 Data Persistence",
                    autoStorage: {
                        title: "💡 Automatic Storage",
                        content: "The Data Manager stores data in JSON without you managing files. Data is automatically organized by <strong>scope</strong>: global, per guild, or per user."
                    },
                    scopes: "The 3 Scopes",
                    global: {
                        title: "🌍 Global",
                        content: "Data shared between all servers. Example: bot config, global blacklist."
                    },
                    guild: {
                        title: "🏠 Guild",
                        content: "Server-specific data. Example: custom prefix, moderation settings."
                    },
                    user: {
                        title: "👤 User",
                        content: "User-specific data. Example: XP, inventory, preferences."
                    },
                    whyScopes: {
                        title: "🤔 Why scopes?",
                        content: "Without scopes, you have to manage keys yourself: <code>data[f\"guild_{guild_id}_user_{user_id}\"]</code>. With scopes, the framework automatically organizes JSON files in separate folders."
                    },
                    fileStructure: "Generated file structure"
                }
            },
            index: {
                badge: "🚀 Version 2.0 Now Available",
                title: "Build Advanced Bots",
                titleGradient: "Without The Chaos",
                subtitle: "A modular, strictly-typed Python framework for Discord. Separate your logic into plugins, handle events with ease, and manage data like a pro.",
                cta: {
                    getStarted: "Get Started",
                    readDocs: "Read Documentation",
                    startBuilding: "Start Building →",
                    starGithub: "⭐ Star on GitHub"
                },
                install: {
                    title: "📦 Install Now",
                    subtitle: "Available on PyPI and Docker Hub",
                    viewPypi: "View on pypi.org →",
                    viewDocker: "View on hub.docker.com →"
                },
                code: {
                    badge: "💻 Simple & Clean",
                    title: "Write Less, Do More",
                    subtitle: "Create a complete plugin in just a few lines"
                },
                features: {
                    title: "Why UnderStar-OS?",
                    modular: {
                        title: "Modular By Design",
                        content: "Don't write one massive file. Split your features into isolated plugins that can be installed, updated, and removed independently."
                    },
                    eventBus: {
                        title: "Event Bus System",
                        content: "Decoupled communication. Plugins can emit and listen to events without tight coupling, ensuring a clean architecture."
                    },
                    persistence: {
                        title: "Smart Persistence",
                        content: "No database setup hell. Built-in JSON storage manager that automatically scopes data by Guild or User."
                    }
                },
                architecture: {
                    badge: "Architecture",
                    title: "How It Works",
                    kernel: { title: "OS Kernel", subtitle: "Manages Lifecycle" },
                    pluginMgr: { title: "Plugin Mgr", subtitle: "Loads Modules" },
                    yourCode: { title: "Your Code", subtitle: "Events & Commands" }
                },
                ctaSection: {
                    title: "Ready to Build Something Amazing?",
                    subtitle: "Join developers building production-ready Discord bots with UnderStar-OS."
                }
            },
            footer: {
                copyright: "© 2025 GalTechDev. Built for Developers.",
                license: "MIT License"
            }
        },
        fr: {
            nav: {
                home: "Accueil",
                getStarted: "Démarrer",
                documentation: "Documentation",
                github: "GitHub"
            },
            getStarted: {
                title: "Démarrer",
                subtitle: "Avant de coder, comprenez comment le framework fonctionne. Vous serez plus efficace et vous saurez débugger.",
                understand: {
                    title: "🧠 Comprendre l'Architecture",
                    whyPlugins: {
                        title: "🤔 Pourquoi un système de plugins ?",
                        content: "Un bot Discord classique devient vite un fichier géant de 2000+ lignes impossible à maintenir. Avec des plugins, chaque fonctionnalité est <strong>isolée</strong> : vous pouvez ajouter, modifier ou supprimer une feature sans toucher au reste du code."
                    },
                    lifecycle: {
                        title: "Le Cycle de Vie",
                        content: "Quand vous lancez votre bot, voici ce qui se passe en coulisses :",
                        diagramTitle: "Cycle de démarrage",
                        step1: { label: "OS.start()", sublabel: "Point d'entrée" },
                        step2: { label: "Scan plugins/", sublabel: "Découverte" },
                        step3: { label: "on_load()", sublabel: "Initialisation" },
                        step4: { label: "on_ready()", sublabel: "Bot connecté" }
                    },
                    remember: {
                        title: "💡 À retenir",
                        content: "<code>on_load()</code> est appelé AVANT la connexion Discord (pour préparer les données), <code>on_ready()</code> est appelé APRÈS (pour les actions qui nécessitent l'API Discord)."
                    },
                    concepts: {
                        title: "Concepts Clés",
                        plugin: {
                            title: "🧩 Plugin",
                            content: "Une classe Python qui hérite de <code>Plugin</code>. Elle a accès au logger, au data manager, et peut déclarer des commandes/events."
                        },
                        eventBus: {
                            title: "⚡ Event Bus",
                            content: "Système de communication entre plugins. Un plugin peut émettre un event, d'autres peuvent l'écouter sans dépendance directe."
                        },
                        dataManager: {
                            title: "💾 Data Manager",
                            content: "Stockage JSON automatique. Pas besoin de gérer les fichiers, le framework scope les données par guild, user, ou global."
                        }
                    }
                },
                installation: {
                    title: "📦 Installation",
                    prerequisites: {
                        title: "✅ Prérequis",
                        content: "Python 3.10+ et git installés sur votre machine. Un token de bot Discord (créé sur le <a href=\"https://discord.com/developers/applications\" target=\"_blank\">Developer Portal</a>)."
                    }
                },
                quickStart: {
                    title: "⚡ Quick Start",
                    createFile: "Créez un fichier <code>main.py</code> :",
                    whatItDoes: {
                        title: "💡 Que fait ce code ?",
                        content: "<strong>Ligne 1</strong> : Importe la classe principale du framework.<br><strong>Ligne 4</strong> : Crée une instance du \"système d'exploitation\" de votre bot.<br><strong>Ligne 5</strong> : Lance la boucle principale. Au premier lancement, le token sera demandé et sauvegardé automatiquement."
                    },
                    runBot: "Lancez le bot :"
                },
                structure: {
                    title: "📁 Structure du Projet",
                    content: "Après le premier lancement, le framework crée cette structure :",
                    warning: {
                        title: "⚠️ Important",
                        content: "Le dossier <code>data/token/</code> contient votre token Discord. <strong>Ne le commitez jamais sur Git !</strong> Ajoutez <code>data/</code> à votre <code>.gitignore</code>."
                    }
                },
                nextSteps: {
                    title: "🎯 Prochaines Étapes",
                    step1: {
                        title: "Créez votre premier plugin",
                        content: "Lisez la section <a href=\"docs.html#plugin-structure\">Plugin Structure</a> pour comprendre comment créer un plugin."
                    },
                    step2: {
                        title: "Ajoutez une commande",
                        content: "Utilisez le décorateur <code>@slash_command</code> pour créer des commandes slash Discord."
                    },
                    step3: {
                        title: "Écoutez les events",
                        content: "Réagissez aux messages, aux réactions, aux membres qui rejoignent avec <code>@listen</code>."
                    },
                    readDocs: "Lire la Documentation Complète →"
                }
            },
            docs: {
                title: "Documentation",
                subtitle: "Référence complète de l'API. Chaque section explique le <strong>comment</strong> et le <strong>pourquoi</strong>.",
                pluginStructure: {
                    title: "🧩 Structure des Plugins",
                    whatIs: {
                        title: "💡 C'est quoi un Plugin ?",
                        content: "Un plugin est une <strong>classe Python</strong> qui représente une fonctionnalité de votre bot. En héritant de <code>Plugin</code>, votre classe reçoit automatiquement accès au logger, au data manager, et peut déclarer des commandes et des listeners."
                    },
                    minimalStructure: "Structure minimale d'un plugin :",
                    lifecycle: {
                        title: "Cycle de vie d'un Plugin",
                        diagramTitle: "Méthodes du cycle de vie",
                        onLoad: { label: "on_load()", sublabel: "Avant connexion" },
                        onReady: { label: "on_ready()", sublabel: "Après connexion" },
                        onUnload: { label: "on_unload()", sublabel: "Arrêt du plugin" }
                    },
                    whySeparate: {
                        title: "🤔 Pourquoi séparer on_load et on_ready ?",
                        content: "<code>on_load()</code> s'exécute AVANT la connexion Discord — utilisez-le pour charger des configs, préparer des données. <code>on_ready()</code> s'exécute APRÈS — utilisez-le pour récupérer des infos de guilds, envoyer des messages de démarrage, etc."
                    },
                    autoAccess: "Ce que vous recevez automatiquement",
                    logger: "Logger pré-configuré avec le nom de votre plugin",
                    data: "Data Manager pour stocker des données persistantes",
                    bot: "Instance du client Discord (après on_ready)"
                },
                commands: {
                    title: "⚡ Commandes Slash",
                    howItWorks: {
                        title: "💡 Comment ça marche ?",
                        content: "Le décorateur <code>@slash_command</code> enregistre votre fonction comme commande Discord. Au démarrage, le framework collecte toutes les commandes et les synchronise avec l'API Discord. Quand un utilisateur tape <code>/votre_commande</code>, Discord appelle votre fonction avec un objet <code>Interaction</code>."
                    },
                    parameters: "Paramètres de commande",
                    parametersDesc: "Ajoutez des paramètres en les déclarant dans la signature de la fonction :",
                    timeout: {
                        title: "⚠️ Timeout de 3 secondes",
                        content: "Discord attend une réponse dans les <strong>3 secondes</strong>. Si votre traitement est long, utilisez <code>interaction.response.defer()</code> puis <code>interaction.followup.send()</code>."
                    }
                },
                events: {
                    title: "👂 Event Listener",
                    eventBus: {
                        title: "💡 L'Event Bus",
                        content: "Discord envoie des \"events\" quand quelque chose se passe (message reçu, membre rejoint, réaction ajoutée...). Le décorateur <code>@listen</code> dit au framework : \"quand cet event arrive, appelle ma fonction\"."
                    },
                    availableEvents: "Events disponibles",
                    onMessage: "Un message est envoyé",
                    onMemberJoin: "Un membre rejoint un serveur",
                    onReactionAdd: "Une réaction est ajoutée",
                    onVoiceState: "Quelqu'un rejoint/quitte un vocal",
                    bestPractice: {
                        title: "✅ Bonne pratique",
                        content: "Toujours vérifier <code>message.author.bot</code> dans <code>ON_MESSAGE</code> pour éviter que votre bot réponde à lui-même en boucle infinie !"
                    }
                },
                tasks: {
                    title: "⏰ Tâches Planifiées",
                    background: {
                        title: "💡 Tâches de fond",
                        content: "Parfois vous voulez exécuter du code à intervalles réguliers (vérifier une API, envoyer un rappel...). Le décorateur <code>@task</code> crée une boucle qui s'exécute automatiquement."
                    },
                    timingOptions: "Options de timing",
                    seconds: "Toutes les 30 secondes",
                    minutes: "Toutes les 5 minutes",
                    hours: "Toutes les heures",
                    errorHandling: {
                        title: "⚠️ Gestion des erreurs",
                        content: "Si votre task crash, elle s'arrête ! Entourez votre code d'un <code>try/except</code> pour éviter qu'une erreur ne stoppe complètement la tâche."
                    }
                },
                data: {
                    title: "💾 Persistance des Données",
                    autoStorage: {
                        title: "💡 Stockage automatique",
                        content: "Le Data Manager stocke des données en JSON sans que vous gériez les fichiers. Les données sont automatiquement organisées par <strong>scope</strong> : global, par guild, ou par user."
                    },
                    scopes: "Les 3 Scopes",
                    global: {
                        title: "🌍 Global",
                        content: "Données partagées entre tous les serveurs. Exemple : config du bot, blacklist globale."
                    },
                    guild: {
                        title: "🏠 Guild",
                        content: "Données spécifiques à un serveur. Exemple : préfixe custom, paramètres de modération."
                    },
                    user: {
                        title: "👤 User",
                        content: "Données spécifiques à un utilisateur. Exemple : XP, inventaire, préférences."
                    },
                    whyScopes: {
                        title: "🤔 Pourquoi des scopes ?",
                        content: "Sans scopes, vous devez gérer vous-même les clés : <code>data[f\"guild_{guild_id}_user_{user_id}\"]</code>. Avec les scopes, le framework organise automatiquement les fichiers JSON dans des dossiers séparés."
                    },
                    fileStructure: "Structure des fichiers générés"
                }
            },
            index: {
                badge: "🚀 Version 2.0 Disponible",
                title: "Créez des Bots Avancés",
                titleGradient: "Sans le Chaos",
                subtitle: "Un framework Python modulaire et strictement typé pour Discord. Séparez votre logique en plugins, gérez les events facilement, et stockez vos données comme un pro.",
                cta: {
                    getStarted: "Démarrer",
                    readDocs: "Lire la Documentation",
                    startBuilding: "Commencer →",
                    starGithub: "⭐ Star sur GitHub"
                },
                install: {
                    title: "📦 Installer Maintenant",
                    subtitle: "Disponible sur PyPI et Docker Hub",
                    viewPypi: "Voir sur pypi.org →",
                    viewDocker: "Voir sur hub.docker.com →"
                },
                code: {
                    badge: "💻 Simple & Propre",
                    title: "Écrivez Moins, Faites Plus",
                    subtitle: "Créez un plugin complet en quelques lignes"
                },
                features: {
                    title: "Pourquoi UnderStar-OS ?",
                    modular: {
                        title: "Modulaire par Design",
                        content: "N'écrivez pas un fichier massif. Séparez vos features en plugins isolés qui peuvent être installés, mis à jour et supprimés indépendamment."
                    },
                    eventBus: {
                        title: "Système Event Bus",
                        content: "Communication découplée. Les plugins peuvent émettre et écouter des events sans couplage fort, garantissant une architecture propre."
                    },
                    persistence: {
                        title: "Persistance Intelligente",
                        content: "Pas de galère de setup de base de données. Gestionnaire de stockage JSON intégré qui scope automatiquement les données par Guild ou User."
                    }
                },
                architecture: {
                    badge: "Architecture",
                    title: "Comment ça Marche",
                    kernel: { title: "OS Kernel", subtitle: "Gère le Cycle de Vie" },
                    pluginMgr: { title: "Plugin Mgr", subtitle: "Charge les Modules" },
                    yourCode: { title: "Votre Code", subtitle: "Events & Commandes" }
                },
                ctaSection: {
                    title: "Prêt à Créer Quelque Chose d'Incroyable ?",
                    subtitle: "Rejoignez les développeurs qui construisent des bots Discord prêts pour la production avec UnderStar-OS."
                }
            },
            footer: {
                copyright: "© 2025 GalTechDev. Fait pour les Développeurs.",
                license: "Licence MIT"
            }
        }
    },

    /**
     * Get current translations
     */
    get translations() {
        return this.allTranslations[this.currentLang] || this.allTranslations.en;
    },

    /**
     * Initialize the i18n system
     */
    init() {
        // Get language from localStorage or detect from browser
        const savedLang = localStorage.getItem('understar-lang');
        const browserLang = navigator.language.slice(0, 2);

        this.currentLang = savedLang ||
            (this.supportedLangs.includes(browserLang) ? browserLang : 'en');

        this.applyTranslations();
        this.updateLangButtons();
    },

    /**
     * Get a translation by key path (e.g., "nav.home")
     */
    t(keyPath) {
        const keys = keyPath.split('.');
        let value = this.translations;

        for (const key of keys) {
            if (value && typeof value === 'object' && key in value) {
                value = value[key];
            } else {
                return null;
            }
        }

        return value;
    },

    /**
     * Apply translations to all elements with data-i18n attribute
     */
    applyTranslations() {
        document.querySelectorAll('[data-i18n]').forEach(element => {
            const key = element.getAttribute('data-i18n');
            const translation = this.t(key);

            if (translation !== null && typeof translation === 'string') {
                const attr = element.getAttribute('data-i18n-attr');
                if (attr) {
                    element.setAttribute(attr, translation);
                } else {
                    element.innerHTML = translation;
                }
            }
        });

        document.documentElement.lang = this.currentLang;
    },

    /**
     * Update language selector buttons
     */
    updateLangButtons() {
        document.querySelectorAll('.lang-btn').forEach(btn => {
            const btnLang = btn.getAttribute('data-lang');
            btn.classList.toggle('active', btnLang === this.currentLang);
        });
    },

    /**
     * Set the current language
     */
    setLanguage(lang) {
        if (!this.supportedLangs.includes(lang)) return;

        this.currentLang = lang;
        localStorage.setItem('understar-lang', lang);
        this.applyTranslations();
        this.updateLangButtons();
    }
};

// Global function for onclick handlers
function setLanguage(lang) {
    i18n.setLanguage(lang);
}

// Initialize on DOM ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => i18n.init());
} else {
    i18n.init();
}
