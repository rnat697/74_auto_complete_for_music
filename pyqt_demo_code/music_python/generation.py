from music_python.MusicTransformer import MusicTransformer
import torch
from miditok  import TokSequence
import os
from midi2audio import FluidSynth
# Uncomment for testing the main in this file
# from prepocessing import Preprocessing
# from MusicTransformer import MusicTransformer

class Generation():
    def __init__(self,promptData, maxGenLength, promptLength, outFileName, tokenizer, promptName):
        self.promptData = promptData
        self.genLength = maxGenLength
        self.promptLength = promptLength
        self.outputFileName = outFileName
        self.tokenizer = tokenizer

        # set context window (i.e. giving the model the last x tokens as context)
        if(promptName == 'Alla Turca'):
            print("Ala Turca")
            self.contextWindow = -80
        elif (promptName == 'Fur Elise'):
            print('Fur Elise')
            self.contextWindow = -50
        else:
            self.contextWindow = -50
            
        self.dirname = os.path.dirname(__file__)
        self.model_name = 'trained_structured_v3.1.1_epoch26'
        self.model_path = self.dirname+'/model/' +self.model_name +'.pth'
        self.gen_results_path = self.dirname + '/outputs/'
        self.out_midi_path = self.gen_results_path + self.outputFileName + '.mid'
        self.out_audio_path = self.gen_results_path + self.outputFileName + '.wav'
        self.token_out_path = self.gen_results_path + self.outputFileName+'.json'
        # self.output_version = '_v10_alla-turca' 

    # Temporary - sanity check to see if files exist
    def checkFolder(self,path):
        files = os.listdir(path)
        for file_name in files:
            print(file_name)

    def loadModel(self):
        num_classes = 512  # Modify the number of MIDI pitch classes
        d_model = 512  # Modify the model dimensionality (updated)
        num_layers = 6 # Modify the number of transformer layers
        num_heads = 8 # Modify the number of attention heads (updated)
        dff = 2048 # Modify the feed-forward dimensionality
        dropout_rate = 0.2  # Modify the dropout rate

        model = MusicTransformer(num_classes, d_model, num_layers, num_heads, dff, dropout_rate)  # Instantiate your model class
        checkpoint = torch.load(self.model_path)
        model.load_state_dict(checkpoint['model_state_dict']) 
        return model
    
    def displayProgress(self, num):
        percentage = (num / self.genLength)*100

        if percentage % 5 == 0:
            print(f"{percentage:.0f}% complete...")

    def generateAudioFile(self):
        print("Converting Midi to Audio...")
        sound_font = os.path.join(self.dirname + "/GeneralUser_GS_1.471/GeneralUser_GS_1.471_/GeneralUser_GS_v1.471.sf2")
        fs = FluidSynth(sound_font=sound_font)
        fs.midi_to_audio(self.out_midi_path,self.out_audio_path)
        print("Generated wav file at: " + self.out_audio_path)


    def generateMusic(self):
        print("Loading model...")
        model = self.loadModel()
        model.eval()  # Set the model to evaluation mode
        print("Model Loaded.")

        initial_seed = self.promptData
        print(initial_seed)

        # Step 4: Generation i guess
        # generatedSequenceNoPrompt = []
        with torch.no_grad():
            print("Loading initial prompt sequence...")
            # take the first x tokens of the song to use as the prompt
            prompt = initial_seed[0]['input_ids'][:self.promptLength] # :50 fur elise, 300:380 nocturne, 300:380 alla-turca but can use :80
            generated_sequence = prompt
            print('Generating music tokens....')
            for i in range(self.genLength):  # desired_length is the length of the sequence you want to generate
                # Prepare the input data based on the generated sequence so far but take the last x tokens
                input_data = generated_sequence[self.contextWindow:] #[-50:] fur elise, [-80:] alla-turca

                # Perform the forward pass
                outputs = model(input_data)

                # Process the outputs and generate the next token
                last_token_logits = outputs[-1:]  # Get the logits for the last token in the sequence
                probabilities = torch.softmax(last_token_logits, dim=-1)  # Apply softmax to obtain token probabilities
                next_token = torch.multinomial(probabilities, num_samples=1)  # Sample the next token based on the probabilities
                next_token = next_token.item()  # Convert the sampled tensor to a scalar value
                
                tokenToAppend = torch.tensor([next_token])
                generated_sequence = torch.cat((generated_sequence, tokenToAppend), dim=0)
                # generatedSequenceNoPrompt = torch.cat((generatedSequenceNoPrompt,tokenToAppend),dim=0)

                self.displayProgress(i)

            print('Generation of tokens finished. Converting tokens back to Midi...')
            tokens = TokSequence(ids=[generated_sequence.tolist()])
            midi = self.tokenizer.tokens_to_midi(tokens)
            midi.instruments[0].name = f'Continuation of original sample ({len(generated_sequence)} tokens)'
           
            print("Converted to Midi. Saving as Midi file...")
            midi.dump(self.out_midi_path) 
            self.tokenizer.save_tokens(generated_sequence, self.token_out_path)
           
            print("Saved as midi file at ", self.out_midi_path)

            self.generateAudioFile()

# if __name__ == "__main__":
   
#     prompt = 'Piano Sonata K545'
#     promptFile = 'Piano-Sonata-K545'
#     # if prompt == 'Alla Turca':
#     #     promptFile = 'alla-turca'
#     # elif prompt == 'Fur Elise':
#     #     promptFile = 'fur-elise'
#     length = 600
#     promptLength = 50
#     name = 'testingk545'
#     preprocess = Preprocessing(promptFile)
#     if(not preprocess.checkAlreadyPreprocessed()):
#         preprocess.preprocessMidi()
#     tokenise = preprocess.loadTokenizerFromJSON()
#     data = preprocess.loadData()

#     generation = Generation(data, maxGenLength=length, promptLength=promptLength, outFileName=name, tokenizer=tokenise, promptName=prompt)
#     generation.generateMusic()