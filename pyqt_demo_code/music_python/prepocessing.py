from miditok.constants import CHORD_MAPS
from miditok import Structured
from pathlib import Path
from music_python.MIDIDataset import MIDIDataset
import os

class Preprocessing:

    def __init__(self, midiName):
        pitch_range = range(21, 109)
        beat_res = {(0, 4): 8, (4, 12): 4}
        nb_velocities = 32
        additional_tokens = {
            'Chord': True, 'Rest': True, 'Tempo': False,
            'rest_range': (2, 4),  # (half,4beats)
            'Program': False,
            "chord_maps": CHORD_MAPS,
            "chord_tokens_with_root_note": True,
        }
        special_tokens = ["PAD", "BOS", "EOS"]
        
        self.tokenizer = Structured(pitch_range, beat_res, nb_velocities, additional_tokens, special_tokens=special_tokens)
        self.midiName = midiName
        self.dirname = os.path.dirname(__file__)
        self.midisFolder= self.dirname +'/midi_input_files/'
        self.preprocessFolder = self.dirname + '/preprocessed/' + self.midiName   # have a folder for each midi file to not overwrite content
        self.target_path = self.midisFolder + midiName + ".mid"
        self.bpeFolder = self.preprocessFolder + '/bpe'
        self.tokens_paths = list(Path(self.bpeFolder).glob("**/*.json"))

    def getTokenizer(self):
        return self.tokenizer
    
    def loadTokenizerFromJSON(self):
        print("Loading tokenizer data...")
        self.tokenizer =  Structured(params=Path(self.bpeFolder+"/BPEparams.json"))
        return self.tokenizer

    # Used when there is a midi upload...
    # Checks if the midi file has already been preprocssed.
    def checkAlreadyPreprocessed(self):
        return os.path.exists(self.bpeFolder)

    # Temporary - sanity check to see if files exist
    def checkFolder(self,path):
        files = os.listdir(path)
        for file_name in files:
            print(file_name)
    
    def loadData(self):
        print("Loading prompt token data...")
        # Only use the token path that has the midi name, not the BPE params
        self.tokens_paths = [path for path in self.tokens_paths if path.name == self.midiName +'.json']
        # Load dataset
        data = MIDIDataset(
            self.tokens_paths, max_seq_len=512, min_seq_len=200, # min_seq_len=384
        )
        return data

    def preprocessMidi(self):    
        # Creates the tokenizer convert MIDIs to tokens
        Path(self.preprocessFolder).mkdir(exist_ok=True, parents=True)
        
        tokens_path = Path(self.preprocessFolder)

        # Look through the midi folder and find all the midi files and make it into an array
        midi_paths = list(Path(self.midisFolder).glob('**/*.mid')) + list(Path(self.midisFolder).glob('**/*.midi')) 

        # Only have the selected midi in the array
        for i in range(len(midi_paths) - 1, -1, -1):
            if str(midi_paths[i]) != str(Path(self.target_path)):
                print(str(midi_paths[i]) + " deleted")
                del midi_paths[i]


        print(midi_paths)
        self.tokenizer.tokenize_midi_dataset(midi_paths, tokens_path)

        # Learn and apply BPE to data we just tokenized
        tokens_bpe_path = Path(self.bpeFolder)
        tokens_bpe_path.mkdir(exist_ok=True, parents=True)
        self.tokenizer.learn_bpe(
            vocab_size=512,
            tokens_paths=list(tokens_path.glob("**/*.json")),
            start_from_empty_voc=False,
        )
        self.tokenizer.apply_bpe_to_dataset(
            tokens_path,
            tokens_bpe_path,
        )
        print("applied bpe")
        # Loads tokens and create data loaders for training
        # tokens_paths = list(Path('/content/drive/MyDrive/Datasets/example').glob("**/*.json"))
        # dataset = MIDIDataset(
        #     self.tokens_paths, max_seq_len=512, min_seq_len=200, # min_seq_len=384
        # )
        self.tokenizer.save_params(Path(self.bpeFolder + '/BPEparams.json'))
        # print(dataset)

# if __name__ == "__main__":
#     midiName = "alla-turca"
#     preprocess = Preprocessing(midiName)
#     if(not preprocess.checkAlreadyPreprocessed()):
#         preprocess.preprocessMidi()
#     tokenise = preprocess.loadTokenizerFromJSON()
