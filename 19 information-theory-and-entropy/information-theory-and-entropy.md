Auteur: Karim Khemiri
Societe de R&D en finance: Khem Kapital

# Information Theory And Entropy

we drew a clean distinction volatility tells you about movement, risk tells you about the probability of rupture conditioned by structure, constraints, and the informational state of the system. so if you want to go further, you have to stop treating "information" as a vague word. you have to give it a form.

in a market, every quote is a message. every tick, every change in spread, every imbalance in volume, every price return is a partial update of the system's state. in other words, the market is not just a place where prices move. it is a source of information emitting continuously. and the moment you look at it like that, entropy stops being a decorative concept. it becomes a direct measure of market readability.

in the Shannon sense, the entropy of a source is written as

$$
H = -\sum_i p_i \log p_i
$$

what this formula measures is not "disorder" in some vague sense. it measures the average uncertainty associated with the possible states emitted by the source. if one state dominates, uncertainty falls. if all states become more or less equivalent, uncertainty rises.

and this is where you have to be precise about the word surprise, because that is what gives the right intuition.

in information theory, the surprise associated with a state \(i\) is

$$
I(i) = -\log(p_i)
$$

if an event is rare, its probability \(p_i\) is small, so its surprise is large. if an event is frequent, its surprise is small. and entropy, at bottom, is just average surprise. so when the states become equiprobable, none of them stands out, none of them really structures the reading, and average surprise becomes maximal. at that point, each observation looks like a draw with no internal hierarchy. the system keeps emitting messages, but those messages no longer organize the reading. they saturate the reading.

that is exactly why a uniform distribution maximizes entropy. not because it would be "chaotic" in a psychological sense, but because it destroys any predominance. nothing is more probable than anything else. so nothing serves as a guide. predictability collapses, not because there is no more data, but because there is no longer any dominant structure in the data.

and that is where the point becomes genuinely useful for risk. what matters is not only the level of \(H\). it is its dynamics.

if you observe

$$
\frac{dH}{dt} > 0
$$

it means that informational uncertainty is increasing. in other words, the market's implicit structure is degrading. the regularities become less clear. the useful correlations fade. the messages coming out of the system look more and more like noise and less and less like readable coding.

from there, the problem is no longer simply "I forecast less well." the problem is deeper. if entropy is rising while you are estimating your conditional probabilities, then the very object you are trying to measure is deforming during the measurement. it is not the formula for risk that breaks. it is the informational support of the formula. your probabilities are still written cleanly on paper, but they stop having operational stability because the system they describe is losing its geometry.

and that is where the most dangerous point appears: the market can look calm, while its entropy is already high.

that is a genuinely critical case. on the surface, price variations are small. so if you only look at realized volatility, you may conclude too quickly that "nothing is happening." but underneath, the market's messages are becoming incoherent, saturated, or simply too flat to carry a reliable reading. prices move little, but they no longer inform properly. and that gap between apparent calm and loss of structure is exactly the kind of zone that prepares a fast transition. because a small shock, in a system that is still readable, can be absorbed. whereas a small shock, in a system that is already informationally saturated, can propagate without dissipation.

in other words: low movement does not mean low risk, if the readability of the system is already degraded.

at this stage, you have to specify what the states \(i\) are. because entropy does not float in a vacuum. it always depends on an alphabet.

that alphabet depends on what you are looking at.

\(i\) can represent tick direction, for example \((+,-,0)\). it can represent discretized return classes. it can represent microstructure states, like a spread and volume configuration. it can represent local patterns on a window if you work with permutation entropy. the exact object does not matter: the logic stays the same. you define a relevant state space. you estimate the probabilities \(p_i\) on a window.

you compute

$$
H = -\sum_i p_i \log p_i
$$

then you look not only at its level, but at its dynamics.

and that is where entropy becomes a readability indicator. not of price. not of return. of readability.

if \(H\) is low, it means a structure stands out. some states dominate, some messages carry more useful information than others, and the system keeps an informational direction.

if \(H\) is high, it means the market is still emitting, but it is no longer ranking. there is signal in the physical sense ticks, prices, volumes but less and less signal in the informational sense, and therefore less and less ability to locate the system's state.

and if \(dH/dt > 0\), then you are not only in an uncertain regime. you are in a regime where uncertainty itself is progressing.

that is why entropy alone is still not enough to make a risk model. it tells you something central the readability of the system but not everything.

to move from detection to modelling, it has to be coupled with two other dimensions.

the first is market memory. in other words: do regimes persist, or do they dissolve immediately? because a market can be unreadable at one instant, but if that loss of readability does not last, it does not mean the same thing as a disorganization that persists. so you need to measure the system's capacity to retain its state, to keep temporal coherence, or on the contrary to forget any past configuration immediately.

the second is the fluidity of information circulation. a message can exist, but be distorted while propagating. it can be delayed, filtered, fragmented, locally absorbed, or amplified in a pathological way. so the real question is not only "how much uncertainty?" but also "does information travel through the system properly?"

and that is where the framework becomes genuinely interesting. entropy tells you whether the system is readable. memory tells you whether that readability or unreadability persists. circulation tells you whether messages travel through the system without distortion or not.

in other words, the clean triad is this:

entropy for readability,

persistence for regime memory,

circulation for signal transmission.

and that triad is what lets you move from a vague intuition of risk to a physical reading of risk. because at that point, the market is no longer just a set of prices. it becomes a system that emits, stores, and transmits information under constraints. and risk is no longer just a size of variation. it becomes the probability that a system loses enough structure, memory, and transmission capacity for a local perturbation to turn into rupture.
