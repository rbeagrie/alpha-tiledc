import os

def path_as_name(path):
    """Default function for naming doit subtasks"""
    return path

def swap_ext(input_filename, new_ext):
    """Remove the last extension from input_filename and replace it with new_ext"""
    
    root, ext = os.path.splitext(input_filename)
    return root + new_ext

def sort_bams(input_dicts):
    """factory function that returns a doit task to sort a list of input bams"""
        
    def doit_task():
    
        for item in input_dicts:
            yield {
                'basename' : 'sort bam',
                'name' : item['name'],
                'file_dep' : [item['bam']],
                'targets' : [swap_ext(item['bam'], '.sorted.bam')],
                'actions' : ['samtools sort %(dependencies)s -o %(targets)s'],
            }
            
    return doit_task
    
def index_bams(input_dicts, auto_sort=True):
    """factory function that returns a doit task to index a list of input bams"""
        
    def doit_task():
        
        for item in input_dicts:
            
            if auto_sort:
                dep = swap_ext(item['bam'], '.sorted.bam')
            else:
                dep = item['bam']
                
            yield {
            'basename' : 'index bam',
            'name' : item['name'],
            'file_dep' : [dep],
            'targets' : [dep + '.bai'],
            'actions' : ['samtools index %(dependencies)s'],
            }
    
    return doit_task

def call_peaks(input_dicts):
    """
    factory function that returns a doit task to peak call a list of input bams
    using MACS2
    """
        
    def doit_task():
    
        for item in input_dicts:
            if not 'sorted_bam' in item:
                item['sorted_bam'] = swap_ext(item['bam'], '.sorted.bam')

            item['bam_index'] = swap_ext(item['sorted_bam'], '.bam.bai')
            
            if 'control_bam' in item:
                item['control_sorted'] = swap_ext(item['control_bam'], '.sorted.bam')
            
            if 'control_sorted' in item:
                item['control_str'] = '-c {}'.format(item['control_sorted'])
            else:
                item['control_str'] = ''

            yield {
            'basename' : 'call peaks',
            'name': item['name'],
            'file_dep' : [item['bam_index']],
            'targets' : [item['peaks_file']],
            'actions' : ['mkdir -pv $(dirname %(targets)s)',
                'macs2 callpeak -t {sorted_bam} {control_str} -n {name} -f BAMPE -g 1.87e9 -q 0.1 '
                '--outdir $(dirname %(targets)s)'.format(**item)],
        }
    
    return doit_task

def merge_bams(input_dicts):
    """
    factory function that merges bamfiles together
    """
    
    def doit_task():
    
        for sample in input_dicts:

            sample_output_dir = os.path.dirname(sample['target'])

            yield {
                'name': sample['name'],
                'file_dep': sample['file_dep'],
                'targets': [sample['target']],
                'actions': ['mkdir -pv {}'.format(sample_output_dir),
                            'samtools merge -f %(targets)s %(dependencies)s']
            }
    
    return doit_task

def link_files(input_dicts):
    """
    factory function that symlinks files
    """
    
    def doit_task():
    
        for sample in input_dicts:

            sample_output_dir = os.path.dirname(sample['target'])

            yield {
                'name': sample['name'],
                'file_dep': [sample['file_dep']],
                'targets': [sample['target']],
                'actions': ['mkdir -pv {}'.format(sample_output_dir),
                            'ln -s %(dependencies)s %(targets)s']
            }
    
    return doit_task