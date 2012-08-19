'''
test_questions.py

Copyright 2012 Andres Riancho

This file is part of w3af, w3af.sourceforge.net .

w3af is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

w3af is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with w3af; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

'''
import os

from nose.plugins.attrib import attr

from core.controllers.w3afCore import w3afCore
from core.controllers.misc.factory import factory

from core.data.options.optionList import optionList


class test_questions(object):

    unique_question_ids = []

    @attr('smoke')
    def test_all_questions(self):
        '''
        This is a very basic test where we perform the following:
            * Create an instance
            * Exercise all getters
            * Exercise all setters
            * Make sure "back" works
        '''
        mod = 'core.controllers.wizard.questions.%s'
        w3af_core = w3afCore()
        
        for filename in os.listdir('core/controllers/wizard/questions/'):
            question_id, ext = os.path.splitext(filename)

            if question_id in ('__init__', '.svn') or ext == '.pyc':
                continue

            klass = mod % question_id
            question_inst = factory( klass, w3af_core )
            
            yield self._test_qid, question_inst
    
    @attr('smoke')
    def _test_qid(self, question_inst):
        '''
        Ahhh, nose's magic of test generators :D
        '''
        orig = question_inst.getQuestionTitle()
        question_inst.setQuestionTitle( 'New' )
        new = question_inst.getQuestionTitle()
        assert 'New' == new
        
        orig = question_inst.getQuestionString()
        question_inst.setQuestionString( 'New' )
        new = question_inst.getQuestionString()
        assert 'New' == new
        
        opt = question_inst.getOptionObjects()
        assert isinstance(opt, optionList) == True
        
        qid = question_inst.getQuestionId()
        assert qid not in self.unique_question_ids
        self.unique_question_ids.append( qid )
            
        question_inst.setPreviouslyAnsweredValues(opt)
        stored_opt = question_inst.getOptionObjects()
        assert id(stored_opt) == id(opt)
